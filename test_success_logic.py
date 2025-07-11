#!/usr/bin/env python3
"""
Script test để kiểm tra logic success mới
"""

def test_success_logic():
    """Test logic success mới"""
    
    test_cases = [
        {
            'name': 'Attack thành công - BLEU giảm',
            'pred_bleu': 25.0,
            'after_bleu': 15.0,
            'change': 2,
            'expected_success': 1
        },
        {
            'name': 'Attack thất bại - BLEU không giảm',
            'pred_bleu': 25.0,
            'after_bleu': 25.0,
            'change': 0,
            'expected_success': 2  # Không có thay đổi
        },
        {
            'name': 'Attack thất bại - BLEU tăng',
            'pred_bleu': 25.0,
            'after_bleu': 30.0,
            'change': 1,
            'expected_success': 4  # Attack thất bại
        },
        {
            'name': 'BLEU ban đầu quá thấp',
            'pred_bleu': 5.0,
            'after_bleu': 5.0,
            'change': 0,
            'expected_success': 3
        }
    ]
    
    print("Test logic success mới:")
    for i, test in enumerate(test_cases):
        # Logic mới
        if test['pred_bleu'] <= 10:  # bleu_theta
            success = 3
        elif test['change'] == 0:
            success = 2
        elif test['after_bleu'] < test['pred_bleu']:
            success = 1
        else:
            success = 4
        
        status = "PASS" if success == test['expected_success'] else "FAIL"
        print(f"   {status} Test {i+1}: {test['name']}")
        print(f"      Expected: {test['expected_success']}, Got: {success}")
        print(f"      Details: pred_bleu={test['pred_bleu']}, after_bleu={test['after_bleu']}, change={test['change']}")
    
    return True

if __name__ == "__main__":
    test_success_logic()
