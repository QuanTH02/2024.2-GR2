#!/usr/bin/env python3
"""
Script để phân tích logic của các field trong file kết quả JSON
Kiểm tra tính nhất quán và đúng đắn của các field
"""

import json
import os
from typing import Dict, List, Any

def analyze_results_logic(file_path: str) -> Dict[str, Any]:
    """Phân tích logic của các field trong file kết quả"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    analysis = {
        'total_samples': len(data),
        'logic_errors': [],
        'inconsistencies': [],
        'field_analysis': {},
        'success_distribution': {},
        'bleu_analysis': {}
    }
    
    # Phân tích từng sample
    for i, sample in enumerate(data):
        sample_errors = []
        
        # 1. Kiểm tra logic của field 'success'
        success = sample.get('success', -1)
        pred_bleu = sample.get('pred_bleu', 0)
        after_attack_bleu = sample.get('after_attack_bleu', 0)
        change = sample.get('change', 0)
        query = sample.get('query', 0)
        changes = sample.get('changes', [])
        
        # Logic kiểm tra success:
        # success = 1: Attack thành công (BLEU giảm)
        # success = 2: Không có thay đổi nào được thực hiện
        # success = 3: Gold output rỗng
        # success = 4: Attack thất bại (BLEU không giảm hoặc tăng)
        
        expected_success = None
        if sample.get('gold_out', '').strip() == '':
            expected_success = 3
        elif change == 0:
            expected_success = 2
        elif after_attack_bleu < pred_bleu:
            expected_success = 1
        else:
            expected_success = 4
            
        if success != expected_success:
            sample_errors.append(f"Success logic error: expected {expected_success}, got {success}")
        
        # 2. Kiểm tra tính nhất quán của change và changes
        if change != len(changes):
            sample_errors.append(f"Change count mismatch: change={change}, len(changes)={len(changes)}")
        
        # 3. Kiểm tra logic của query
        if change > 0 and query == 0:
            sample_errors.append(f"Query should not be 0 when changes exist: change={change}, query={query}")
        
        # 4. Kiểm tra BLEU scores
        if pred_bleu < 0 or pred_bleu > 100:
            sample_errors.append(f"Invalid pred_bleu: {pred_bleu}")
        if after_attack_bleu < 0 or after_attack_bleu > 100:
            sample_errors.append(f"Invalid after_attack_bleu: {after_attack_bleu}")
        
        # 5. Kiểm tra input và adv
        input_text = sample.get('input', '')
        adv_text = sample.get('adv', '')
        
        # Nếu có changes, adv phải khác input
        if change > 0 and input_text == adv_text:
            sample_errors.append(f"Adv should be different from input when changes exist")
        
        # 6. Kiểm tra imp_words
        imp_words = sample.get('imp_words', {})
        if change > 0 and not imp_words:
            sample_errors.append(f"Imp_words should not be empty when changes exist")
        
        if sample_errors:
            analysis['logic_errors'].append({
                'sample_index': i,
                'errors': sample_errors,
                'sample': sample
            })
        
        # Thống kê success distribution
        success_type = {
            1: 'Attack Success',
            2: 'No Changes',
            3: 'Empty Gold',
            4: 'Attack Failed'
        }.get(success, f'Unknown ({success})')
        
        analysis['success_distribution'][success_type] = analysis['success_distribution'].get(success_type, 0) + 1
    
    # Phân tích BLEU scores
    pred_bleus = [s.get('pred_bleu', 0) for s in data]
    after_bleus = [s.get('after_attack_bleu', 0) for s in data]
    
    analysis['bleu_analysis'] = {
        'pred_bleu_stats': {
            'min': min(pred_bleus),
            'max': max(pred_bleus),
            'avg': sum(pred_bleus) / len(pred_bleus),
            'zero_count': pred_bleus.count(0)
        },
        'after_bleu_stats': {
            'min': min(after_bleus),
            'max': max(after_bleus),
            'avg': sum(after_bleus) / len(after_bleus),
            'zero_count': after_bleus.count(0)
        },
        'bleu_decrease_count': sum(1 for p, a in zip(pred_bleus, after_bleus) if a < p),
        'bleu_increase_count': sum(1 for p, a in zip(pred_bleus, after_bleus) if a > p),
        'bleu_same_count': sum(1 for p, a in zip(pred_bleus, after_bleus) if a == p)
    }
    
    # Phân tích field consistency
    analysis['field_analysis'] = {
        'samples_with_empty_input': sum(1 for s in data if not s.get('input', '').strip()),
        'samples_with_empty_gold': sum(1 for s in data if not s.get('gold_out', '').strip()),
        'samples_with_changes': sum(1 for s in data if s.get('change', 0) > 0),
        'samples_with_imp_words': sum(1 for s in data if s.get('imp_words', {})),
        'avg_query_count': sum(s.get('query', 0) for s in data) / len(data)
    }
    
    return analysis

def print_analysis_report(analysis: Dict[str, Any]):
    """In báo cáo phân tích"""
    print("=" * 60)
    print("PHÂN TÍCH LOGIC KẾT QUẢ JSON")
    print("=" * 60)
    
    print(f"\n📊 TỔNG QUAN:")
    print(f"   - Tổng số samples: {analysis['total_samples']}")
    print(f"   - Số lỗi logic: {len(analysis['logic_errors'])}")
    
    print(f"\n🎯 PHÂN BỐ SUCCESS:")
    for success_type, count in analysis['success_distribution'].items():
        percentage = (count / analysis['total_samples']) * 100
        print(f"   - {success_type}: {count} ({percentage:.1f}%)")
    
    print(f"\n📈 PHÂN TÍCH BLEU SCORES:")
    bleu = analysis['bleu_analysis']
    print(f"   - Pred BLEU - Min: {bleu['pred_bleu_stats']['min']:.2f}, Max: {bleu['pred_bleu_stats']['max']:.2f}, Avg: {bleu['pred_bleu_stats']['avg']:.2f}")
    print(f"   - After BLEU - Min: {bleu['after_bleu_stats']['min']:.2f}, Max: {bleu['after_bleu_stats']['max']:.2f}, Avg: {bleu['after_bleu_stats']['avg']:.2f}")
    print(f"   - BLEU giảm: {bleu['bleu_decrease_count']} samples")
    print(f"   - BLEU tăng: {bleu['bleu_increase_count']} samples")
    print(f"   - BLEU không đổi: {bleu['bleu_same_count']} samples")
    
    print(f"\n🔍 PHÂN TÍCH FIELD:")
    field = analysis['field_analysis']
    print(f"   - Samples có input rỗng: {field['samples_with_empty_input']}")
    print(f"   - Samples có gold output rỗng: {field['samples_with_empty_gold']}")
    print(f"   - Samples có thay đổi: {field['samples_with_changes']}")
    print(f"   - Samples có imp_words: {field['samples_with_imp_words']}")
    print(f"   - Trung bình số query: {field['avg_query_count']:.1f}")
    
    if analysis['logic_errors']:
        print(f"\n❌ LỖI LOGIC PHÁT HIỆN:")
        for error in analysis['logic_errors'][:10]:  # Chỉ hiển thị 10 lỗi đầu
            print(f"   Sample {error['sample_index']}:")
            for err in error['errors']:
                print(f"     - {err}")
        
        if len(analysis['logic_errors']) > 10:
            print(f"     ... và {len(analysis['logic_errors']) - 10} lỗi khác")
    else:
        print(f"\n✅ KHÔNG CÓ LỖI LOGIC NÀO PHÁT HIỆN!")

def main():
    """Main function"""
    file_path = "output/translation/codet5/codebert/cs_java_test_run/66.json"
    
    if not os.path.exists(file_path):
        print(f"❌ File không tồn tại: {file_path}")
        return
    
    print("🔍 Đang phân tích file kết quả...")
    analysis = analyze_results_logic(file_path)
    print_analysis_report(analysis)
    
    # Lưu báo cáo chi tiết
    report_file = "analysis_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Báo cáo chi tiết đã lưu vào: {report_file}")

if __name__ == "__main__":
    main() 