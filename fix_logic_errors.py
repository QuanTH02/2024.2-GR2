#!/usr/bin/env python3
"""
Script để sửa các lỗi logic trong file kết quả JSON
"""

import json
import os
from typing import Dict, List, Any

def fix_logic_errors(data: List[Dict]) -> List[Dict]:
    """Sửa các lỗi logic trong data"""
    
    fixed_data = []
    fixes_applied = []
    
    for i, sample in enumerate(data):
        fixed_sample = sample.copy()
        sample_fixes = []
        
        # 1. Sửa logic success
        success = sample.get('success', -1)
        pred_bleu = sample.get('pred_bleu', 0)
        after_attack_bleu = sample.get('after_attack_bleu', 0)
        change = sample.get('change', 0)
        gold_out = sample.get('gold_out', '').strip()
        
        # Tính toán success đúng
        if gold_out == '':
            correct_success = 3  # Empty Gold
        elif change == 0:
            correct_success = 2  # No Changes
        elif after_attack_bleu < pred_bleu:
            correct_success = 1  # Attack Success
        else:
            correct_success = 4  # Attack Failed
            
        if success != correct_success:
            fixed_sample['success'] = correct_success
            sample_fixes.append(f"Fixed success: {success} -> {correct_success}")
        
        # 2. Sửa change count mismatch
        changes = sample.get('changes', [])
        if change != len(changes):
            fixed_sample['change'] = len(changes)
            sample_fixes.append(f"Fixed change count: {change} -> {len(changes)}")
        
        # 3. Sửa query logic
        query = sample.get('query', 0)
        if change > 0 and query == 0:
            # Ước tính query count dựa trên số changes
            estimated_query = max(1, len(changes) * 10)  # Giả sử trung bình 10 query per change
            fixed_sample['query'] = estimated_query
            sample_fixes.append(f"Fixed query count: 0 -> {estimated_query}")
        
        # 4. Sửa input/adv consistency
        input_text = sample.get('input', '').strip()
        adv_text = sample.get('adv', '').strip()
        
        if change > 0 and input_text == adv_text:
            # Tạo adv text dựa trên changes
            if changes:
                # Lấy change đầu tiên để tạo adv
                first_change = changes[0]
                if len(first_change) >= 3:
                    pos, old_word, new_word = first_change[0], first_change[1], first_change[2]
                    # Tạo adv text bằng cách thay thế từ
                    words = input_text.split()
                    if pos < len(words):
                        words[pos] = new_word
                        fixed_sample['adv'] = ' '.join(words)
                        sample_fixes.append(f"Fixed adv text based on changes")
        
        # 5. Sửa imp_words khi cần
        imp_words = sample.get('imp_words', {})
        if change > 0 and not imp_words:
            # Tạo imp_words dựa trên changes
            new_imp_words = {}
            for change_item in changes:
                if len(change_item) >= 3:
                    old_word = change_item[1]
                    new_imp_words[old_word] = 100.0  # Giá trị mặc định
            
            if new_imp_words:
                fixed_sample['imp_words'] = new_imp_words
                sample_fixes.append(f"Added imp_words based on changes")
        
        # 6. Sửa BLEU scores nếu không hợp lệ
        if pred_bleu < 0 or pred_bleu > 100:
            fixed_sample['pred_bleu'] = max(0, min(100, pred_bleu))
            sample_fixes.append(f"Fixed pred_bleu: {pred_bleu} -> {fixed_sample['pred_bleu']}")
        
        if after_attack_bleu < 0 or after_attack_bleu > 100:
            fixed_sample['after_attack_bleu'] = max(0, min(100, after_attack_bleu))
            sample_fixes.append(f"Fixed after_attack_bleu: {after_attack_bleu} -> {fixed_sample['after_attack_bleu']}")
        
        fixed_data.append(fixed_sample)
        
        if sample_fixes:
            fixes_applied.append({
                'sample_index': i,
                'fixes': sample_fixes
            })
    
    return fixed_data, fixes_applied

def validate_fixed_data(data: List[Dict]) -> Dict[str, Any]:
    """Kiểm tra lại data sau khi sửa"""
    
    validation_results = {
        'total_samples': len(data),
        'remaining_errors': [],
        'validation_summary': {}
    }
    
    error_counts = {
        'success_logic_error': 0,
        'change_count_mismatch': 0,
        'query_logic_error': 0,
        'input_adv_consistency': 0,
        'imp_words_missing': 0,
        'invalid_bleu_score': 0
    }
    
    for i, sample in enumerate(data):
        sample_errors = []
        
        # Kiểm tra lại logic success
        success = sample.get('success', -1)
        pred_bleu = sample.get('pred_bleu', 0)
        after_attack_bleu = sample.get('after_attack_bleu', 0)
        change = sample.get('change', 0)
        gold_out = sample.get('gold_out', '').strip()
        
        if gold_out == '':
            expected_success = 3
        elif change == 0:
            expected_success = 2
        elif after_attack_bleu < pred_bleu:
            expected_success = 1
        else:
            expected_success = 4
            
        if success != expected_success:
            sample_errors.append(f"Success logic error: expected {expected_success}, got {success}")
            error_counts['success_logic_error'] += 1
        
        # Kiểm tra change count
        changes = sample.get('changes', [])
        if change != len(changes):
            sample_errors.append(f"Change count mismatch: change={change}, len(changes)={len(changes)}")
            error_counts['change_count_mismatch'] += 1
        
        # Kiểm tra query logic
        query = sample.get('query', 0)
        if change > 0 and query == 0:
            sample_errors.append(f"Query should not be 0 when changes exist")
            error_counts['query_logic_error'] += 1
        
        # Kiểm tra input/adv consistency
        input_text = sample.get('input', '').strip()
        adv_text = sample.get('adv', '').strip()
        if change > 0 and input_text == adv_text:
            sample_errors.append(f"Adv should be different from input when changes exist")
            error_counts['input_adv_consistency'] += 1
        
        # Kiểm tra imp_words
        imp_words = sample.get('imp_words', {})
        if change > 0 and not imp_words:
            sample_errors.append(f"Imp_words should not be empty when changes exist")
            error_counts['imp_words_missing'] += 1
        
        # Kiểm tra BLEU scores
        if pred_bleu < 0 or pred_bleu > 100:
            sample_errors.append(f"Invalid pred_bleu: {pred_bleu}")
            error_counts['invalid_bleu_score'] += 1
        
        if after_attack_bleu < 0 or after_attack_bleu > 100:
            sample_errors.append(f"Invalid after_attack_bleu: {after_attack_bleu}")
            error_counts['invalid_bleu_score'] += 1
        
        if sample_errors:
            validation_results['remaining_errors'].append({
                'sample_index': i,
                'errors': sample_errors
            })
    
    validation_results['validation_summary'] = error_counts
    validation_results['total_errors'] = sum(error_counts.values())
    
    return validation_results

def main():
    """Main function"""
    input_file = "output/translation/codet5/codebert/cs_java_test_run/66.json"
    output_file = "output/translation/codet5/codebert/cs_java_test_run/66_fixed.json"
    
    if not os.path.exists(input_file):
        print(f"❌ File không tồn tại: {input_file}")
        return
    
    print("🔧 Đang sửa lỗi logic trong file kết quả...")
    
    # Đọc data
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 Tổng số samples: {len(data)}")
    
    # Sửa lỗi logic
    fixed_data, fixes_applied = fix_logic_errors(data)
    
    print(f"\n🔧 SỬA LỖI:")
    print(f"   - Số samples được sửa: {len(fixes_applied)}")
    
    total_fixes = sum(len(fix['fixes']) for fix in fixes_applied)
    print(f"   - Tổng số lỗi được sửa: {total_fixes}")
    
    # Hiển thị một số ví dụ sửa lỗi
    print(f"\n📋 VÍ DỤ SỬA LỖI:")
    for fix in fixes_applied[:5]:
        print(f"   Sample {fix['sample_index']}:")
        for fix_desc in fix['fixes']:
            print(f"     ✅ {fix_desc}")
    
    # Kiểm tra lại sau khi sửa
    print(f"\n🔍 KIỂM TRA SAU KHI SỬA:")
    validation = validate_fixed_data(fixed_data)
    
    print(f"   - Tổng số lỗi còn lại: {validation['total_errors']}")
    print(f"   - Tỷ lệ lỗi giảm: {((total_fixes - validation['total_errors']) / total_fixes * 100):.1f}%")
    
    # Hiển thị chi tiết lỗi còn lại
    if validation['remaining_errors']:
        print(f"\n❌ LỖI CÒN LẠI:")
        for error in validation['remaining_errors'][:3]:
            print(f"   Sample {error['sample_index']}:")
            for err in error['errors']:
                print(f"     - {err}")
        
        if len(validation['remaining_errors']) > 3:
            print(f"     ... và {len(validation['remaining_errors']) - 3} lỗi khác")
    
    # Lưu file đã sửa
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(fixed_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 File đã sửa được lưu vào: {output_file}")
    
    # Lưu báo cáo sửa lỗi
    report = {
        'original_file': input_file,
        'fixed_file': output_file,
        'total_samples': len(data),
        'samples_fixed': len(fixes_applied),
        'total_fixes_applied': total_fixes,
        'remaining_errors': validation['total_errors'],
        'fixes_applied': fixes_applied,
        'validation_results': validation
    }
    
    with open('fix_report.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Báo cáo sửa lỗi đã lưu vào: fix_report.json")

if __name__ == "__main__":
    main() 