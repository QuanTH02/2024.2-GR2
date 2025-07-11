#!/usr/bin/env python3
"""
Script phân tích chi tiết các lỗi logic trong kết quả JSON
và đưa ra giải pháp khắc phục
"""

import json
import os
from typing import Dict, List, Any

def detailed_logic_analysis(file_path: str) -> Dict[str, Any]:
    """Phân tích chi tiết logic và đưa ra giải pháp"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    analysis = {
        'total_samples': len(data),
        'critical_errors': [],
        'logic_issues': [],
        'data_quality_issues': [],
        'recommendations': []
    }
    
    # Phân tích từng sample
    for i, sample in enumerate(data):
        sample_issues = []
        
        # 1. Phân tích field 'success'
        success = sample.get('success', -1)
        pred_bleu = sample.get('pred_bleu', 0)
        after_attack_bleu = sample.get('after_attack_bleu', 0)
        change = sample.get('change', 0)
        query = sample.get('query', 0)
        changes = sample.get('changes', [])
        gold_out = sample.get('gold_out', '').strip()
        input_text = sample.get('input', '').strip()
        adv_text = sample.get('adv', '').strip()
        
        # Logic kiểm tra success
        if gold_out == '':
            expected_success = 3  # Empty Gold
        elif change == 0:
            expected_success = 2  # No Changes
        elif after_attack_bleu < pred_bleu:
            expected_success = 1  # Attack Success
        else:
            expected_success = 4  # Attack Failed
            
        if success != expected_success:
            sample_issues.append({
                'type': 'success_logic_error',
                'description': f'Success logic error: expected {expected_success}, got {success}',
                'details': {
                    'pred_bleu': pred_bleu,
                    'after_bleu': after_attack_bleu,
                    'change': change,
                    'gold_empty': gold_out == '',
                    'bleu_decreased': after_attack_bleu < pred_bleu
                }
            })
        
        # 2. Kiểm tra tính nhất quán của changes
        if change != len(changes):
            sample_issues.append({
                'type': 'change_count_mismatch',
                'description': f'Change count mismatch: change={change}, len(changes)={len(changes)}',
                'details': {
                    'change_field': change,
                    'changes_length': len(changes),
                    'changes_content': changes
                }
            })
        
        # 3. Kiểm tra logic của query
        if change > 0 and query == 0:
            sample_issues.append({
                'type': 'query_logic_error',
                'description': f'Query should not be 0 when changes exist',
                'details': {
                    'change': change,
                    'query': query,
                    'changes': changes
                }
            })
        
        # 4. Kiểm tra input và adv consistency
        if change > 0 and input_text == adv_text:
            sample_issues.append({
                'type': 'input_adv_consistency',
                'description': f'Adv should be different from input when changes exist',
                'details': {
                    'input': input_text,
                    'adv': adv_text,
                    'changes': changes
                }
            })
        
        # 5. Kiểm tra imp_words
        imp_words = sample.get('imp_words', {})
        if change > 0 and not imp_words:
            sample_issues.append({
                'type': 'imp_words_missing',
                'description': f'Imp_words should not be empty when changes exist',
                'details': {
                    'change': change,
                    'imp_words': imp_words,
                    'changes': changes
                }
            })
        
        # 6. Kiểm tra BLEU scores validity
        if pred_bleu < 0 or pred_bleu > 100:
            sample_issues.append({
                'type': 'invalid_bleu_score',
                'description': f'Invalid pred_bleu: {pred_bleu}',
                'details': {'pred_bleu': pred_bleu}
            })
        
        if after_attack_bleu < 0 or after_attack_bleu > 100:
            sample_issues.append({
                'type': 'invalid_bleu_score',
                'description': f'Invalid after_attack_bleu: {after_attack_bleu}',
                'details': {'after_bleu': after_attack_bleu}
            })
        
        # 7. Kiểm tra data quality
        if not input_text and change > 0:
            sample_issues.append({
                'type': 'data_quality',
                'description': f'Empty input but has changes',
                'details': {
                    'input': input_text,
                    'change': change,
                    'changes': changes
                }
            })
        
        if sample_issues:
            analysis['logic_issues'].append({
                'sample_index': i,
                'issues': sample_issues,
                'sample_data': {
                    'success': success,
                    'pred_bleu': pred_bleu,
                    'after_bleu': after_attack_bleu,
                    'change': change,
                    'query': query,
                    'input': input_text,
                    'adv': adv_text,
                    'gold_out': gold_out
                }
            })
    
    # Phân loại lỗi
    error_types = {}
    for issue in analysis['logic_issues']:
        for problem in issue['issues']:
            error_type = problem['type']
            if error_type not in error_types:
                error_types[error_type] = []
            error_types[error_type].append(problem['description'])
    
    analysis['error_summary'] = error_types
    
    # Đưa ra khuyến nghị
    recommendations = []
    
    if 'success_logic_error' in error_types:
        recommendations.append({
            'issue': 'Logic lỗi trong field success',
            'count': len(error_types['success_logic_error']),
            'solution': 'Cần sửa lại logic xác định success trong code attack'
        })
    
    if 'change_count_mismatch' in error_types:
        recommendations.append({
            'issue': 'Số lượng change không khớp với changes array',
            'count': len(error_types['change_count_mismatch']),
            'solution': 'Cần đồng bộ hóa việc đếm changes và cập nhật field change'
        })
    
    if 'query_logic_error' in error_types:
        recommendations.append({
            'issue': 'Query = 0 khi có changes',
            'count': len(error_types['query_logic_error']),
            'solution': 'Cần đảm bảo query > 0 khi có thay đổi được thực hiện'
        })
    
    if 'input_adv_consistency' in error_types:
        recommendations.append({
            'issue': 'Input và adv giống nhau khi có changes',
            'count': len(error_types['input_adv_consistency']),
            'solution': 'Cần kiểm tra logic tạo adversarial example'
        })
    
    analysis['recommendations'] = recommendations
    
    return analysis

def print_detailed_report(analysis: Dict[str, Any]):
    """In báo cáo chi tiết"""
    print("=" * 80)
    print("PHÂN TÍCH CHI TIẾT LỖI LOGIC TRONG KẾT QUẢ JSON")
    print("=" * 80)
    
    print(f"\n📊 TỔNG QUAN:")
    print(f"   - Tổng số samples: {analysis['total_samples']}")
    print(f"   - Số samples có lỗi: {len(analysis['logic_issues'])}")
    print(f"   - Tỷ lệ lỗi: {(len(analysis['logic_issues']) / analysis['total_samples']) * 100:.1f}%")
    
    print(f"\n🔍 PHÂN LOẠI LỖI:")
    for error_type, errors in analysis['error_summary'].items():
        print(f"   - {error_type}: {len(errors)} lỗi")
        # Hiển thị 3 ví dụ đầu tiên
        for i, error in enumerate(errors[:3]):
            print(f"     {i+1}. {error}")
        if len(errors) > 3:
            print(f"     ... và {len(errors) - 3} lỗi khác")
    
    print(f"\n💡 KHUYẾN NGHỊ KHẮC PHỤC:")
    for rec in analysis['recommendations']:
        print(f"   - {rec['issue']} ({rec['count']} lỗi)")
        print(f"     Giải pháp: {rec['solution']}")
    
    # Hiển thị một số ví dụ cụ thể
    print(f"\n📋 VÍ DỤ LỖI CỤ THỂ:")
    for i, issue in enumerate(analysis['logic_issues'][:5]):
        print(f"\n   Sample {issue['sample_index']}:")
        sample_data = issue['sample_data']
        print(f"     Success: {sample_data['success']}")
        print(f"     Pred BLEU: {sample_data['pred_bleu']:.2f}")
        print(f"     After BLEU: {sample_data['after_bleu']:.2f}")
        print(f"     Change: {sample_data['change']}")
        print(f"     Query: {sample_data['query']}")
        print(f"     Input: '{sample_data['input']}'")
        print(f"     Adv: '{sample_data['adv']}'")
        print(f"     Gold: '{sample_data['gold_out']}'")
        
        for problem in issue['issues']:
            print(f"     ❌ {problem['description']}")

def main():
    """Main function"""
    file_path = "output/translation/codet5/codebert/cs_java_test_run/66.json"
    
    if not os.path.exists(file_path):
        print(f"❌ File không tồn tại: {file_path}")
        return
    
    print("🔍 Đang phân tích chi tiết file kết quả...")
    analysis = detailed_logic_analysis(file_path)
    print_detailed_report(analysis)
    
    # Lưu báo cáo chi tiết
    report_file = "detailed_analysis_report.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Báo cáo chi tiết đã lưu vào: {report_file}")

if __name__ == "__main__":
    main() 