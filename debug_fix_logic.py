#!/usr/bin/env python3
"""
Script debug để kiểm tra lỗi trong quá trình sửa logic
"""

import json
import os
import traceback

def main():
    """Main function"""
    input_file = "output/translation/codet5/codebert/cs_java_test_run/66.json"
    
    print("🔍 Debug: Kiểm tra file...")
    print(f"File exists: {os.path.exists(input_file)}")
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"✅ Loaded {len(data)} samples")
        
        # Kiểm tra sample đầu tiên
        if data:
            first_sample = data[0]
            print(f"📋 Sample 0:")
            print(f"   Success: {first_sample.get('success')}")
            print(f"   Pred BLEU: {first_sample.get('pred_bleu')}")
            print(f"   After BLEU: {first_sample.get('after_attack_bleu')}")
            print(f"   Change: {first_sample.get('change')}")
            print(f"   Query: {first_sample.get('query')}")
            print(f"   Input: '{first_sample.get('input')}'")
            print(f"   Adv: '{first_sample.get('adv')}'")
            print(f"   Gold: '{first_sample.get('gold_out')}'")
            print(f"   Changes: {first_sample.get('changes')}")
            print(f"   Imp_words: {first_sample.get('imp_words')}")
        
        # Phân tích logic
        print(f"\n🔍 Phân tích logic...")
        success_errors = 0
        change_errors = 0
        query_errors = 0
        
        for i, sample in enumerate(data):
            success = sample.get('success', -1)
            pred_bleu = sample.get('pred_bleu', 0)
            after_attack_bleu = sample.get('after_attack_bleu', 0)
            change = sample.get('change', 0)
            query = sample.get('query', 0)
            changes = sample.get('changes', [])
            gold_out = sample.get('gold_out', '').strip()
            
            # Kiểm tra success logic
            if gold_out == '':
                expected_success = 3
            elif change == 0:
                expected_success = 2
            elif after_attack_bleu < pred_bleu:
                expected_success = 1
            else:
                expected_success = 4
                
            if success != expected_success:
                success_errors += 1
                if success_errors <= 3:  # Chỉ hiển thị 3 lỗi đầu
                    print(f"   Sample {i}: Success error - expected {expected_success}, got {success}")
            
            # Kiểm tra change count
            if change != len(changes):
                change_errors += 1
                if change_errors <= 3:
                    print(f"   Sample {i}: Change count error - change={change}, len(changes)={len(changes)}")
            
            # Kiểm tra query logic
            if change > 0 and query == 0:
                query_errors += 1
                if query_errors <= 3:
                    print(f"   Sample {i}: Query error - change={change}, query={query}")
        
        print(f"\n📊 Tổng kết lỗi:")
        print(f"   - Success logic errors: {success_errors}")
        print(f"   - Change count errors: {change_errors}")
        print(f"   - Query logic errors: {query_errors}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main() 