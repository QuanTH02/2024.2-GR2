# HƯỚNG DẪN CHẠY EXPERIMENTS THEO BÁO CÁO

## 📋 **TỔNG QUAN**

Hướng dẫn này sẽ giúp bạn chạy tất cả các experiments cần thiết để trả lời 4 Research Questions (RQ) trong báo cáo.

## 🎯 **4 RESEARCH QUESTIONS CẦN TRẢ LỜI**

### **RQ1**: CodeAttack có thể tấn công hiệu quả và chuyển giao tốt giữa các nhiệm vụ và ngôn ngữ lập trình khác nhau hay không?

### **RQ2**: Các đoạn mã đối kháng được sinh ra có đảm bảo chất lượng cao (hiệu quả, khó nhận biết, đồng nhất với mã gốc) không?

### **RQ3**: Nếu giới hạn số lượng thay đổi đầu vào, CodeAttack còn giữ được tính hiệu quả không?

### **RQ4**: Mỗi thành phần trong CodeAttack có vai trò như thế nào trong hiệu quả tấn công?

## 🚀 **PHẦN 1: THIẾT LẬP MÔI TRƯỜNG**

### **1.1 Cài đặt dependencies**
```bash
# Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# Hoặc nếu dùng conda
conda env create -f requirements.yml
conda activate codeattack
```

### **1.2 Kiểm tra cấu trúc thư mục**
```bash
# Đảm bảo có đầy đủ các thư mục
ls -la checkpoints/
ls -la data/
ls -la configs/
```

## 📊 **PHẦN 2: EXPERIMENTS CHO RQ1 - HIỆU QUẢ VÀ CHUYỂN GIAO**

### **2.1 Code Translation Experiments**

#### **Java → C# Translation**
```bash
# CodeT5 as victim model
py codeattack.py \
    --attack_model codebert \
    --victim_model codet5 \
    --task translation \
    --lang java_cs_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq1_translation_java_cs_codet5 \
    --theta 0.4

# CodeBERT as victim model  
py codeattack.py \
    --attack_model codebert \
    --victim_model codebert \
    --task translation \
    --lang java_cs_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq1_translation_java_cs_codebert \
    --theta 0.4

# GraphCodeBERT as victim model
py codeattack.py \
    --attack_model codebert \
    --victim_model graphcodebert \
    --task translation \
    --lang java_cs_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq1_translation_java_cs_graphcodebert \
    --input_lang java \
    --theta 0.4
```

#### **C# → Java Translation**
```bash
# CodeT5 as victim model
py codeattack.py \
    --attack_model codebert \
    --victim_model codet5 \
    --task translation \
    --lang cs_java_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq1_translation_cs_java_codet5 \
    --theta 0.4

# CodeBERT as victim model
py codeattack.py \
    --attack_model codebert \
    --victim_model codebert \
    --task translation \
    --lang cs_java_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq1_translation_cs_java_codebert \
    --theta 0.4

# GraphCodeBERT as victim model
py codeattack.py \
    --attack_model codebert \
    --victim_model graphcodebert \
    --task translation \
    --lang cs_java_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq1_translation_cs_java_graphcodebert \
    --input_lang c_sharp \
    --theta 0.4
```

### **2.2 Code Summarization Experiments**

#### **py Summarization**
```bash
# CodeT5 as victim model
py codeattack.py \
    --attack_model codebert \
    --victim_model codet5 \
    --task summarize \
    --lang python_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq1_summarize_python_codet5 \
    --theta 0.4

# CodeBERT as victim model
py codeattack.py \
    --attack_model codebert \
    --victim_model codebert \
    --task summarize \
    --lang python_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq1_summarize_python_codebert \
    --theta 0.4
```

#### **Java Summarization**
```bash
# CodeT5 as victim model
py codeattack.py \
    --attack_model codebert \
    --victim_model codet5 \
    --task summarize \
    --lang java_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq1_summarize_java_codet5 \
    --theta 0.4

# CodeBERT as victim model
py codeattack.py \
    --attack_model codebert \
    --victim_model codebert \
    --task summarize \
    --lang java_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq1_summarize_java_codebert \
    --theta 0.4
```

#### **PHP Summarization**
```bash
# CodeT5 as victim model
py codeattack.py \
    --attack_model codebert \
    --victim_model codet5 \
    --task summarize \
    --lang php_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq1_summarize_php_codet5 \
    --theta 0.4

# CodeBERT as victim model
py codeattack.py \
    --attack_model codebert \
    --victim_model codebert \
    --task summarize \
    --lang php_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq1_summarize_php_codebert \
    --theta 0.4
```

### **2.3 Code Refinement Experiments**

#### **Java Small Refinement**
```bash
# CodeT5 as victim model
py codeattack.py \
    --attack_model codebert \
    --victim_model codet5 \
    --task refinement \
    --lang java_small_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq1_refinement_java_small_codet5 \
    --theta 0.4

# CodeBERT as victim model
py codeattack.py \
    --attack_model codebert \
    --victim_model codebert \
    --task refinement \
    --lang java_small_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq1_refinement_java_small_codebert \
    --theta 0.4

# GraphCodeBERT as victim model
py codeattack.py \
    --attack_model codebert \
    --victim_model graphcodebert \
    --task refinement \
    --lang java_small_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq1_refinement_java_small_graphcodebert \
    --input_lang java \
    --theta 0.4
```

## 🔬 **PHẦN 3: EXPERIMENTS CHO RQ2 - CHẤT LƯỢNG MÃ ĐỐI KHÁNG**

### **3.1 So sánh với Baseline Methods**

#### **TextFooler Comparison**
```bash
# TextFooler attack on CodeT5
py codeattack.py \
    --attack_model textfooler \
    --victim_model codet5 \
    --task translation \
    --lang java_cs_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq2_textfooler_java_cs_codet5 \
    --theta 0.4

# TextFooler attack on CodeBERT
py codeattack.py \
    --attack_model textfooler \
    --victim_model codebert \
    --task translation \
    --lang java_cs_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq2_textfooler_java_cs_codebert \
    --theta 0.4
```

#### **BERT-Attack Comparison**
```bash
# BERT-Attack on CodeT5
py codeattack.py \
    --attack_model bertattack \
    --victim_model codet5 \
    --task translation \
    --lang java_cs_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq2_bertattack_java_cs_codet5 \
    --theta 0.4

# BERT-Attack on CodeBERT
py codeattack.py \
    --attack_model bertattack \
    --victim_model codebert \
    --task translation \
    --lang java_cs_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq2_bertattack_java_cs_codebert \
    --theta 0.4
```

### **3.2 Quality Assessment**
```bash
# Chạy script đánh giá chất lượng
py evaluate_quality.py \
    --results_dir output/rq2_textfooler_java_cs_codet5 \
    --output_file quality_assessment_rq2.json
```

## ⚙️ **PHẦN 4: EXPERIMENTS CHO RQ3 - GIỚI HẠN THAY ĐỔI**

### **4.1 Varying Change Limits**

#### **Low Change Limit (10%)**
```bash
py codeattack.py \
    --attack_model codebert \
    --victim_model codet5 \
    --task translation \
    --lang java_cs_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq3_change_limit_10 \
    --theta 0.1
```

#### **Medium Change Limit (20%)**
```bash
py codeattack.py \
    --attack_model codebert \
    --victim_model codet5 \
    --task translation \
    --lang java_cs_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq3_change_limit_20 \
    --theta 0.2
```

#### **High Change Limit (40%)**
```bash
py codeattack.py \
    --attack_model codebert \
    --victim_model codet5 \
    --task translation \
    --lang java_cs_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq3_change_limit_40 \
    --theta 0.4
```

#### **Very High Change Limit (60%)**
```bash
py codeattack.py \
    --attack_model codebert \
    --victim_model codet5 \
    --task translation \
    --lang java_cs_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq3_change_limit_60 \
    --theta 0.6
```

## 🔧 **PHẦN 5: EXPERIMENTS CHO RQ4 - THÀNH PHẦN ANALYSIS**

### **5.1 Important Words vs Random Words**

#### **Using Important Words (Default)**
```bash
py codeattack.py \
    --attack_model codebert \
    --victim_model codet5 \
    --task translation \
    --lang java_cs_large \
    --use_ast 0 \
    --use_dfg 0 \
    --use_imp 1 \
    --out_dirname rq4_important_words \
    --theta 0.4
```

#### **Using Random Words**
```bash
py codeattack.py \
    --attack_model codebert \
    --victim_model codet5 \
    --task translation \
    --lang java_cs_large \
    --use_ast 0 \
    --use_dfg 0 \
    --use_imp 0 \
    --out_dirname rq4_random_words \
    --theta 0.4
```

### **5.2 AST Constraints Analysis**

#### **With AST Constraints**
```bash
py codeattack.py \
    --attack_model codebert \
    --victim_model codet5 \
    --task translation \
    --lang java_cs_large \
    --use_ast 1 \
    --use_dfg 0 \
    --out_dirname rq4_with_ast \
    --theta 0.4
```

#### **Without AST Constraints**
```bash
py codeattack.py \
    --attack_model codebert \
    --victim_model codet5 \
    --task translation \
    --lang java_cs_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq4_without_ast \
    --theta 0.4
```

### **5.3 DFG Constraints Analysis**

#### **With DFG Constraints**
```bash
py codeattack.py \
    --attack_model codebert \
    --victim_model codet5 \
    --task translation \
    --lang java_cs_large \
    --use_ast 0 \
    --use_dfg 1 \
    --out_dirname rq4_with_dfg \
    --theta 0.4
```

#### **Without DFG Constraints**
```bash
py codeattack.py \
    --attack_model codebert \
    --victim_model codet5 \
    --task translation \
    --lang java_cs_large \
    --use_ast 0 \
    --use_dfg 0 \
    --out_dirname rq4_without_dfg \
    --theta 0.4
```

## 📈 **PHẦN 6: PHÂN TÍCH KẾT QUẢ**

### **6.1 Tạo Script Phân Tích Tổng Hợp**
```python
# Tạo file: analyze_all_results.py
import json
import os
import pandas as pd
from typing import Dict, List

def analyze_all_experiments():
    """
    Phân tích tất cả kết quả experiments
    """
    results = {}
    
    # Phân tích RQ1 - Transferability
    results['rq1'] = analyze_transferability()
    
    # Phân tích RQ2 - Quality
    results['rq2'] = analyze_quality()
    
    # Phân tích RQ3 - Change Limits
    results['rq3'] = analyze_change_limits()
    
    # Phân tích RQ4 - Components
    results['rq4'] = analyze_components()
    
    # Tạo báo cáo tổng hợp
    generate_comprehensive_report(results)
    
    return results

def analyze_transferability():
    """Phân tích RQ1 - Transferability across tasks and languages"""
    # Implementation here
    pass

def analyze_quality():
    """Phân tích RQ2 - Quality of adversarial code"""
    # Implementation here
    pass

def analyze_change_limits():
    """Phân tích RQ3 - Effect of change limits"""
    # Implementation here
    pass

def analyze_components():
    """Phân tích RQ4 - Component analysis"""
    # Implementation here
    pass

def generate_comprehensive_report(results):
    """Tạo báo cáo tổng hợp"""
    # Implementation here
    pass
```

### **6.2 Chạy Phân Tích**
```bash
# Phân tích tất cả kết quả
py analyze_all_results.py

# Tạo báo cáo chi tiết
py generate_detailed_report.py
```

## 🎯 **PHẦN 7: SCRIPT TỰ ĐỘNG HÓA**

### **7.1 Script Chạy Tất Cả Experiments**
```bash
#!/bin/bash
# run_all_experiments.sh

echo "Starting all experiments for CodeAttack paper..."

# RQ1 Experiments
echo "Running RQ1 - Transferability experiments..."
py run_rq1_experiments.py

# RQ2 Experiments  
echo "Running RQ2 - Quality experiments..."
py run_rq2_experiments.py

# RQ3 Experiments
echo "Running RQ3 - Change limit experiments..."
py run_rq3_experiments.py

# RQ4 Experiments
echo "Running RQ4 - Component analysis experiments..."
py run_rq4_experiments.py

# Analysis
echo "Running comprehensive analysis..."
py analyze_all_results.py

echo "All experiments completed!"
```

### **7.2 Chạy Script Tự Động**
```bash
# Cấp quyền thực thi
chmod +x run_all_experiments.sh

# Chạy tất cả experiments
./run_all_experiments.sh
```

## 📊 **PHẦN 8: KẾT QUẢ DỰ KIẾN**

### **8.1 Metrics Sẽ Thu Được**

#### **RQ1 - Transferability**
- Success Rate across tasks: ~40-60%
- Success Rate across languages: ~35-55%
- Transferability score: ~0.7-0.9

#### **RQ2 - Quality**
- CodeBLEU preservation: ~80-90%
- Semantic similarity: ~0.8-0.95
- Human evaluation score: ~7-9/10

#### **RQ3 - Change Limits**
- Success Rate with 10% changes: ~20-30%
- Success Rate with 40% changes: ~40-60%
- Optimal change threshold: ~30-40%

#### **RQ4 - Components**
- Important words vs Random: ~2-3x better
- AST constraints impact: ~10-20% improvement
- DFG constraints impact: ~5-15% improvement

### **8.2 Files Kết Quả**
```
output/
├── rq1_transferability/
│   ├── translation_results.json
│   ├── summarization_results.json
│   └── refinement_results.json
├── rq2_quality/
│   ├── codeattack_vs_baselines.json
│   └── quality_assessment.json
├── rq3_change_limits/
│   ├── change_limit_analysis.json
│   └── optimal_threshold.json
├── rq4_components/
│   ├── component_analysis.json
│   └── ablation_study.json
└── comprehensive_report/
    ├── final_results.json
    ├── tables.csv
    └── figures/
```

## ⚠️ **LƯU Ý QUAN TRỌNG**

### **8.1 Thời Gian Chạy**
- **RQ1**: ~6-8 giờ (18 experiments)
- **RQ2**: ~4-6 giờ (8 experiments)  
- **RQ3**: ~2-3 giờ (4 experiments)
- **RQ4**: ~3-4 giờ (6 experiments)
- **Tổng**: ~15-21 giờ

### **8.2 Tài Nguyên Cần Thiết**
- **GPU**: NVIDIA RTX 3080 hoặc tương đương
- **RAM**: 16GB+
- **Storage**: 50GB+ cho kết quả
- **CPU**: 8 cores+

### **8.3 Monitoring**
```bash
# Theo dõi tiến trình
watch -n 10 'ps aux | grep python'

# Kiểm tra GPU usage
nvidia-smi

# Kiểm tra disk space
df -h
```

## ✅ **KẾT LUẬN**

Với hướng dẫn này, bạn có thể:

1. **Chạy đầy đủ** tất cả experiments cần thiết
2. **Trả lời đầy đủ** 4 Research Questions
3. **Tạo báo cáo** chi tiết và chuyên nghiệp
4. **Đánh giá hiệu quả** của CodeAttack một cách toàn diện

**Thời gian thực hiện**: 2-3 ngày với setup đầy đủ
**Kết quả**: Báo cáo nghiên cứu chất lượng cao 