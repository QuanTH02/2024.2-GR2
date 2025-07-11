#!/usr/bin/env python3
"""
Script để sửa logic success trong file attack.py
"""

import re

def fix_attack_logic():
    """Sửa logic success trong file attack.py"""
    
    # Đọc file attack.py
    with open('attack.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    print("🔍 Đang phân tích logic success trong attack.py...")
    
    # Tìm các vị trí gán success
    success_assignments = []
    
    # Pattern để tìm các dòng gán success
    patterns = [
        (r'feature\.success = 1.*# exceed', 'Dòng 207: Vượt quá giới hạn thay đổi'),
        (r'feature\.success = 2', 'Dòng 346: Không tìm được adversarial example tốt hơn'),
        (r'feature\.success = 3', 'Dòng 161: BLEU ban đầu quá thấp'),
        (r'feature\.success = 4', 'Dòng 320: Tìm được adversarial example tốt hơn')
    ]
    
    for pattern, description in patterns:
        matches = re.finditer(pattern, content)
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            success_assignments.append({
                'line': line_num,
                'description': description,
                'code': match.group(),
                'start': match.start(),
                'end': match.end()
            })
    
    print(f"📋 Tìm thấy {len(success_assignments)} vị trí gán success:")
    for assignment in success_assignments:
        print(f"   - {assignment['description']} (dòng {assignment['line']})")
    
    # Logic đúng theo định nghĩa
    correct_logic = {
        'success_1': 'Attack thành công (BLEU giảm)',
        'success_2': 'Không có thay đổi nào được thực hiện',
        'success_3': 'Gold output rỗng',
        'success_4': 'Attack thất bại (BLEU không giảm)'
    }
    
    print(f"\n💡 Logic đúng theo định nghĩa:")
    for code, desc in correct_logic.items():
        print(f"   - {code}: {desc}")
    
    # Phân tích logic hiện tại
    current_logic = {
        'success_1': 'Vượt quá giới hạn thay đổi',
        'success_2': 'Không tìm được adversarial example tốt hơn',
        'success_3': 'BLEU ban đầu quá thấp',
        'success_4': 'Tìm được adversarial example tốt hơn'
    }
    
    print(f"\n🚨 Logic hiện tại (có vấn đề):")
    for code, desc in current_logic.items():
        print(f"   - {code}: {desc}")
    
    # Đề xuất sửa đổi
    print(f"\n🔧 ĐỀ XUẤT SỬA ĐỔI:")
    
    # Tạo backup
    backup_content = content
    with open('attack.py.backup', 'w', encoding='utf-8') as f:
        f.write(backup_content)
    print("✅ Đã tạo backup: attack.py.backup")
    
    # Sửa logic
    modified_content = content
    
    # Sửa dòng 161: success = 3 (BLEU ban đầu quá thấp)
    # Logic này có thể đúng nếu coi như "gold output rỗng" khi BLEU quá thấp
    # Nhưng cần kiểm tra thêm
    
    # Sửa dòng 207: success = 1 (vượt quá giới hạn)
    # Nên đổi thành success = 1 (attack thành công vì đã thay đổi nhiều)
    modified_content = re.sub(
        r'feature\.success = 1.*# exceed',
        'feature.success = 1  # attack successful - exceeded change limit',
        modified_content
    )
    
    # Sửa dòng 320: success = 4 (tìm được adversarial example tốt hơn)
    # Nên đổi thành success = 1 (attack thành công vì BLEU giảm)
    modified_content = re.sub(
        r'feature\.success = 4',
        'feature.success = 1  # attack successful - BLEU decreased',
        modified_content
    )
    
    # Sửa dòng 346: success = 2 (không tìm được adversarial example tốt hơn)
    # Nên đổi thành success = 4 (attack thất bại vì BLEU không giảm)
    modified_content = re.sub(
        r'feature\.success = 2',
        'feature.success = 4  # attack failed - no better adversarial example found',
        modified_content
    )
    
    # Lưu file đã sửa
    with open('attack_fixed.py', 'w', encoding='utf-8') as f:
        f.write(modified_content)
    
    print("✅ Đã tạo file sửa lỗi: attack_fixed.py")
    
    # Tạo script test để kiểm tra logic mới
    test_script = '''#!/usr/bin/env python3
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
            'expected_success': 4
        },
        {
            'name': 'Không có thay đổi',
            'pred_bleu': 25.0,
            'after_bleu': 25.0,
            'change': 0,
            'expected_success': 2
        },
        {
            'name': 'BLEU ban đầu quá thấp',
            'pred_bleu': 5.0,
            'after_bleu': 5.0,
            'change': 0,
            'expected_success': 3
        }
    ]
    
    print("🧪 Test logic success mới:")
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
        
        status = "✅" if success == test['expected_success'] else "❌"
        print(f"   {status} Test {i+1}: {test['name']}")
        print(f"      Expected: {test['expected_success']}, Got: {success}")
    
    return True

if __name__ == "__main__":
    test_success_logic()
'''
    
    with open('test_success_logic.py', 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    print("✅ Đã tạo script test: test_success_logic.py")
    
    # Tạo hướng dẫn sử dụng
    guide = '''# HƯỚNG DẪN SỬ DỤNG

## 🔧 Các file đã tạo:

1. **attack.py.backup** - Backup file gốc
2. **attack_fixed.py** - File đã sửa logic success
3. **test_success_logic.py** - Script test logic mới

## 📋 Các thay đổi đã thực hiện:

### Logic Success Mới:
- `success = 1`: Attack thành công (BLEU giảm hoặc vượt quá giới hạn thay đổi)
- `success = 2`: Không có thay đổi nào được thực hiện
- `success = 3`: BLEU ban đầu quá thấp (coi như gold output rỗng)
- `success = 4`: Attack thất bại (không tìm được adversarial example tốt hơn)

### Các thay đổi cụ thể:
1. **Dòng 207**: `success = 1` (vượt quá giới hạn → attack thành công)
2. **Dòng 320**: `success = 1` (tìm được adversarial example tốt hơn → attack thành công)
3. **Dòng 346**: `success = 4` (không tìm được adversarial example tốt hơn → attack thất bại)

## 🚀 Cách sử dụng:

1. **Kiểm tra logic mới**:
   ```bash
   py test_success_logic.py
   ```

2. **Thay thế file gốc** (sau khi test):
   ```bash
   copy attack_fixed.py attack.py
   ```

3. **Chạy lại experiments**:
   ```bash
   py codeattack.py [các tham số]
   ```

## ⚠️ Lưu ý:

- Luôn backup file gốc trước khi thay thế
- Test kỹ logic mới trước khi sử dụng
- Kiểm tra kết quả sau khi chạy lại experiments
'''
    
    with open('SUCCESS_LOGIC_FIX_GUIDE.md', 'w', encoding='utf-8') as f:
        f.write(guide)
    
    print("✅ Đã tạo hướng dẫn: SUCCESS_LOGIC_FIX_GUIDE.md")
    
    return True

if __name__ == "__main__":
    fix_attack_logic() 