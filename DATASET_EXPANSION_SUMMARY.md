# CodeAttack Dataset Expansion Summary

## 🎯 **Vấn đề ban đầu**
- Dữ liệu test chỉ có **5 mẫu** cho mỗi task
- Kết quả chỉ có **5 kết quả** tương ứng
- Cần nhiều dữ liệu hơn để đánh giá hiệu quả

## 🚀 **Giải pháp đã thực hiện**

### 1. **Mở rộng dữ liệu test**
- **Tạo script `expand_test_data.py`**: Mở rộng từ 1 → 5 mẫu cho mỗi task
- **Tạo script `create_large_test_dataset.py`**: Tạo dataset lớn với 30+ mẫu cho mỗi task

### 2. **Cấu trúc dữ liệu mới**

#### **Translation (Dịch code)**
- **Small dataset**: 5 mẫu Java ↔ C#
- **Large dataset**: 30 mẫu Java ↔ C#
- **File**: `data/code_translation/large.java-cs.txt.java` và `.cs`

#### **Summarization (Tóm tắt code)**
- **Small dataset**: 5 mẫu cho mỗi ngôn ngữ
- **Large dataset**: 30 mẫu cho mỗi ngôn ngữ
- **Ngôn ngữ**: Java, Python, PHP, JavaScript, Go, Ruby
- **File**: `data/code_summarization/code-to-text/{lang}/large.jsonl`

#### **Refinement (Sửa lỗi code)**
- **Small dataset**: 5 cặp buggy-fixed
- **Large dataset**: 26 cặp buggy-fixed
- **File**: `data/code_refinement/{size}/large.buggy-fixed.{buggy|fixed}`

### 3. **Cập nhật cấu hình**
- **File**: `configs/config_data.yaml`
- **Thêm các option mới**: `java_cs_large`, `java_large`, `java_small_large`, etc.

### 4. **Sửa lỗi kỹ thuật**
- **Lỗi Unicode**: Thêm `encoding='utf-8'` cho file I/O
- **Lỗi Tensor**: Sửa `torch.tensor()` warnings
- **Xử lý ký tự đặc biệt**: Clean Unicode characters
- **Lỗi BLEU**: Sửa `ZeroDivisionError` khi `reference_length = 0`

## 📊 **Kết quả đạt được**

### **Trước khi mở rộng:**
```
Translation: 1 mẫu → 1 kết quả
Summarization: 1 mẫu → 1 kết quả  
Refinement: 1 mẫu → 1 kết quả
```

### **Sau khi mở rộng:**
```
Translation: 30 mẫu → 30 kết quả
Summarization: 30 mẫu × 6 ngôn ngữ → 180 kết quả
Refinement: 26 mẫu → 26 kết quả
```

## 🛠 **Cách sử dụng**

### **1. Chạy với dataset nhỏ (5 mẫu)**
```bash
py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs --use_ast 0 --use_dfg 0 --out_dirname test_run --theta 0.4
```

### **2. Chạy với dataset lớn (30 mẫu)**
```bash
py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --out_dirname large_test --theta 0.4
```

### **3. Các task khác với dataset lớn**
```bash
# Summarization
py codeattack.py --attack_model codebert --victim_model codet5 --task summarize --lang java_large --use_ast 0 --use_dfg 0 --out_dirname large_summary --theta 0.4

# Refinement  
py codeattack.py --attack_model codebert --victim_model codet5 --task refinement --lang java_small_large --use_ast 0 --use_dfg 0 --out_dirname large_refine --theta 0.4
```

## 📁 **Scripts đã tạo**

1. **`expand_test_data.py`** - Mở rộng dataset cơ bản
2. **`create_large_test_dataset.py`** - Tạo dataset lớn
3. **`demo_large_dataset.py`** - Demo và kiểm tra dataset
4. **`run_large_dataset_test.py`** - Test toàn diện
5. **`quick_test.py`** - Test nhanh để kiểm tra lỗi
6. **`test_bleu_fix.py`** - Test sửa lỗi BLEU
7. **`test_bleu_edge_cases.py`** - Test edge cases của BLEU

## 🔧 **Lỗi đã sửa**

### **1. Lỗi Unicode**
```python
# Trước
with open(output_fn, 'w') as f:

# Sau  
with open(output_fn, 'w', encoding='utf-8') as f:
```

### **2. Lỗi Tensor**
```python
# Trước
pred_score = torch.sum(torch.tensor(pred_scores))

# Sau
pred_score = torch.sum(pred_scores)
```

### **3. Xử lý ký tự đặc biệt**
```python
def clean_text(text):
    text = text.replace('\u2019', "'").replace('\u2018', "'")
    text = ''.join(char for char in text if ord(char) < 128 or char.isprintable())
    return text.strip()
```

### **4. Sửa lỗi BLEU**
```python
# Handle division by zero in ratio calculation
if reference_length == 0:
    if translation_length == 0:
        ratio = 1.0  # Both are empty, perfect match
    else:
        ratio = 0.0  # Reference is empty but translation is not
else:
    ratio = float(translation_length) / reference_length

# Handle division by zero in brevity penalty
if ratio > 1.0:
    bp = 1.
elif ratio == 0.0:
    bp = 0.0  # Handle case where ratio is 0
else:
    bp = math.exp(1 - 1. / ratio)
```

## 📈 **Lợi ích**

1. **Đánh giá chính xác hơn**: Nhiều mẫu test hơn
2. **Kết quả đáng tin cậy**: Thống kê tốt hơn
3. **So sánh hiệu quả**: Có thể so sánh giữa các model
4. **Nghiên cứu sâu hơn**: Phân tích chi tiết hơn

## 🎯 **Kết luận**

- ✅ **Đã mở rộng dataset từ 5 → 30+ mẫu**
- ✅ **Đã sửa tất cả lỗi kỹ thuật**
- ✅ **Đã cập nhật cấu hình**
- ✅ **Đã tạo scripts hỗ trợ**

**Bây giờ bạn có thể chạy CodeAttack với dataset lớn và nhận được nhiều kết quả hơn!** 