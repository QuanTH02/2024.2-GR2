# CÁC LỆNH MỘT DÒNG ĐỂ COPY PASTE

## 🚀 **CÁC LỆNH CƠ BẢN**

### **Test Translation (Java → C#)**
```bash
py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs --use_ast 0 --use_dfg 0 --out_dirname test_translation_codet5 --theta 0.4
```

### **Test Summarization (Java)**
```bash
py codeattack.py --attack_model codebert --victim_model codebert --task summarize --lang java --use_ast 0 --use_dfg 0 --out_dirname test_summarize_codebert --theta 0.4
```

### **Test Refinement (Java Small)**
```bash
py codeattack.py --attack_model codebert --victim_model graphcodebert --task refinement --lang java_small --use_ast 0 --use_dfg 0 --out_dirname test_refinement_graphcodebert --input_lang java --theta 0.4
```

## 📊 **RQ1 - TRANSFERABILITY EXPERIMENTS**

### **Translation Experiments**

#### **Java → C# với CodeT5**
```bash
py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --out_dirname rq1_translation_java_cs_codet5 --theta 0.4
```

#### **Java → C# với CodeBERT**
```bash
py codeattack.py --attack_model codebert --victim_model codebert --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --out_dirname rq1_translation_java_cs_codebert --theta 0.4
```

#### **Java → C# với GraphCodeBERT**
```bash
py codeattack.py --attack_model codebert --victim_model graphcodebert --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --out_dirname rq1_translation_java_cs_graphcodebert --input_lang java --theta 0.4
```

#### **C# → Java với CodeT5**
```bash
py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang cs_java_large --use_ast 0 --use_dfg 0 --out_dirname rq1_translation_cs_java_codet5 --theta 0.4
```

#### **C# → Java với CodeBERT**
```bash
py codeattack.py --attack_model codebert --victim_model codebert --task translation --lang cs_java_large --use_ast 0 --use_dfg 0 --out_dirname rq1_translation_cs_java_codebert --theta 0.4
```

#### **C# → Java với GraphCodeBERT**
```bash
py codeattack.py --attack_model codebert --victim_model graphcodebert --task translation --lang cs_java_large --use_ast 0 --use_dfg 0 --out_dirname rq1_translation_cs_java_graphcodebert --input_lang c_sharp --theta 0.4
```

### **Summarization Experiments**

#### **Python Summarization với CodeT5**
```bash
py codeattack.py --attack_model codebert --victim_model codet5 --task summarize --lang python_large --use_ast 0 --use_dfg 0 --out_dirname rq1_summarize_python_codet5 --theta 0.4
```

#### **Python Summarization với CodeBERT**
```bash
py codeattack.py --attack_model codebert --victim_model codebert --task summarize --lang python_large --use_ast 0 --use_dfg 0 --out_dirname rq1_summarize_python_codebert --theta 0.4
```

#### **Java Summarization với CodeT5**
```bash
py codeattack.py --attack_model codebert --victim_model codet5 --task summarize --lang java_large --use_ast 0 --use_dfg 0 --out_dirname rq1_summarize_java_codet5 --theta 0.4
```

#### **Java Summarization với CodeBERT**
```bash
py codeattack.py --attack_model codebert --victim_model codebert --task summarize --lang java_large --use_ast 0 --use_dfg 0 --out_dirname rq1_summarize_java_codebert --theta 0.4
```

#### **PHP Summarization với CodeT5**
```bash
py codeattack.py --attack_model codebert --victim_model codet5 --task summarize --lang php_large --use_ast 0 --use_dfg 0 --out_dirname rq1_summarize_php_codet5 --theta 0.4
```

#### **PHP Summarization với CodeBERT**
```bash
py codeattack.py --attack_model codebert --victim_model codebert --task summarize --lang php_large --use_ast 0 --use_dfg 0 --out_dirname rq1_summarize_php_codebert --theta 0.4
```

### **Refinement Experiments**

#### **Java Small Refinement với CodeT5**
```bash
py codeattack.py --attack_model codebert --victim_model codet5 --task refinement --lang java_small_large --use_ast 0 --use_dfg 0 --out_dirname rq1_refinement_java_small_codet5 --theta 0.4
```

#### **Java Small Refinement với CodeBERT**
```bash
py codeattack.py --attack_model codebert --victim_model codebert --task refinement --lang java_small_large --use_ast 0 --use_dfg 0 --out_dirname rq1_refinement_java_small_codebert --theta 0.4
```

#### **Java Small Refinement với GraphCodeBERT**
```bash
py codeattack.py --attack_model codebert --victim_model graphcodebert --task refinement --lang java_small_large --use_ast 0 --use_dfg 0 --out_dirname rq1_refinement_java_small_graphcodebert --input_lang java --theta 0.4
```

## 🔬 **RQ2 - QUALITY COMPARISON EXPERIMENTS**

### **TextFooler Comparison**

#### **TextFooler vs CodeT5**
```bash
py codeattack.py --attack_model textfooler --victim_model codet5 --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --out_dirname rq2_textfooler_java_cs_codet5 --theta 0.4
```

#### **TextFooler vs CodeBERT**
```bash
py codeattack.py --attack_model textfooler --victim_model codebert --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --out_dirname rq2_textfooler_java_cs_codebert --theta 0.4
```

### **BERT-Attack Comparison**

#### **BERT-Attack vs CodeT5**
```bash
py codeattack.py --attack_model bertattack --victim_model codet5 --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --out_dirname rq2_bertattack_java_cs_codet5 --theta 0.4
```

#### **BERT-Attack vs CodeBERT**
```bash
py codeattack.py --attack_model bertattack --victim_model codebert --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --out_dirname rq2_bertattack_java_cs_codebert --theta 0.4
```

## ⚙️ **RQ3 - CHANGE LIMIT EXPERIMENTS**

### **Varying Change Limits**

#### **10% Change Limit**
```bash
py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --out_dirname rq3_change_limit_10 --theta 0.1
```

#### **20% Change Limit**
```bash
py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --out_dirname rq3_change_limit_20 --theta 0.2
```

#### **40% Change Limit**
```bash
py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --out_dirname rq3_change_limit_40 --theta 0.4
```

#### **60% Change Limit**
```bash
py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --out_dirname rq3_change_limit_60 --theta 0.6
```

## 🔧 **RQ4 - COMPONENT ANALYSIS EXPERIMENTS**

### **Important Words vs Random Words**

#### **Important Words Selection**
```bash
py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --use_imp 1 --out_dirname rq4_important_words --theta 0.4
```

#### **Random Words Selection**
```bash
py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --use_imp 0 --out_dirname rq4_random_words --theta 0.4
```

### **AST Constraints Analysis**

#### **With AST Constraints**
```bash
py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs_large --use_ast 1 --use_dfg 0 --out_dirname rq4_with_ast --theta 0.4
```

#### **Without AST Constraints**
```bash
py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --out_dirname rq4_without_ast --theta 0.4
```

### **DFG Constraints Analysis**

#### **With DFG Constraints**
```bash
py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs_large --use_ast 0 --use_dfg 1 --out_dirname rq4_with_dfg --theta 0.4
```

#### **Without DFG Constraints**
```bash
py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --out_dirname rq4_without_dfg --theta 0.4
```

## 📈 **ANALYSIS COMMANDS**

### **Phân tích kết quả**
```bash
py analyze_all_results.py
```

### **Tạo báo cáo chi tiết**
```bash
py generate_detailed_report.py
```

### **Chạy script tự động**
```bash
py quick_start_experiments.py
```

### **Chạy experiment đơn lẻ**
```bash
py run_single_experiment.py
```

## 🎯 **LỆNH NHANH CHO NGƯỜI MỚI**

### **Bắt đầu với Translation**
```bash
py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs --use_ast 0 --use_dfg 0 --out_dirname my_first_experiment --theta 0.4
```

### **Bắt đầu với Summarization**
```bash
py codeattack.py --attack_model codebert --victim_model codet5 --task summarize --lang python_large --use_ast 0 --use_dfg 0 --out_dirname my_first_summarization --theta 0.4
```

### **Bắt đầu với Refinement**
```bash
py codeattack.py --attack_model codebert --victim_model codet5 --task refinement --lang java_small_large --use_ast 0 --use_dfg 0 --out_dirname my_first_refinement --theta 0.4
```

## ⚠️ **LƯU Ý**

1. **Thay đổi `--out_dirname`** để tránh ghi đè kết quả
2. **Kiểm tra GPU** trước khi chạy
3. **Đảm bảo có dataset** trong thư mục `data/`
4. **Đảm bảo có checkpoints** trong thư mục `checkpoints/`

## 📁 **KẾT QUẢ SẼ ĐƯỢC LƯU Ở**
```
output/
├── my_first_experiment/
├── rq1_translation_java_cs_codet5/
├── rq2_textfooler_java_cs_codet5/
├── rq3_change_limit_10/
└── rq4_important_words/
``` 