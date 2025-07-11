# HƯỚNG DẪN SỬ DỤNG

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
