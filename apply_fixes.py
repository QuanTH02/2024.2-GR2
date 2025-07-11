#!/usr/bin/env python3
"""
Script để áp dụng sửa đổi logic một cách an toàn
"""

import os
import shutil
import json
from datetime import datetime

def apply_fixes():
    """Áp dụng sửa đổi logic một cách an toàn"""
    
    print("AP DUNG SUA DOI LOGIC")
    print("=" * 50)
    
    # Kiểm tra các file cần thiết
    required_files = [
        'attack.py.backup',
        'attack_fixed.py',
        'test_success_logic.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"Thieu cac file can thiet: {missing_files}")
        print("Vui long chay fix_attack_logic.py truoc")
        return False
    
    print("Tat ca file can thiet da co")
    
    # Tạo backup timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"backup_{timestamp}"
    os.makedirs(backup_dir, exist_ok=True)
    
    print(f"Tao backup tai: {backup_dir}")
    
    # Backup file hiện tại
    if os.path.exists('attack.py'):
        shutil.copy2('attack.py', os.path.join(backup_dir, 'attack.py'))
        print("Da backup attack.py hien tai")
    
    # Backup kết quả cũ nếu có
    output_dirs = [
        'output/translation/codet5/codebert/cs_java_test_run',
        'output/summarization',
        'output/refinement'
    ]
    
    for output_dir in output_dirs:
        if os.path.exists(output_dir):
            backup_output_dir = os.path.join(backup_dir, output_dir)
            os.makedirs(os.path.dirname(backup_output_dir), exist_ok=True)
            shutil.copytree(output_dir, backup_output_dir)
            print(f"Da backup {output_dir}")
    
    # Test logic mới
    print("\nTest logic moi...")
    try:
        import subprocess
        result = subprocess.run(['py', 'test_success_logic.py'], 
                              capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print("Logic test passed")
            print(result.stdout)
        else:
            print("Logic test failed")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"Loi khi test logic: {e}")
        return False
    
    # Áp dụng sửa đổi
    print("\nAp dung sua doi...")
    try:
        shutil.copy2('attack_fixed.py', 'attack.py')
        print("Da thay the attack.py voi phien ban da sua")
    except Exception as e:
        print(f"Loi khi thay the file: {e}")
        return False
    
    # Tạo file log
    log_data = {
        'timestamp': timestamp,
        'action': 'apply_logic_fixes',
        'files_backed_up': [
            'attack.py',
            'output/translation/codet5/codebert/cs_java_test_run'
        ],
        'changes_applied': [
            'Fixed success logic in attack.py',
            'Updated success code assignments'
        ],
        'backup_location': backup_dir
    }
    
    with open('fix_application_log.json', 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)
    
    print("Da tao log: fix_application_log.json")
    
    # Tạo script chạy lại experiments
    run_experiment_script = f'''#!/usr/bin/env python3
"""
Script để chạy lại experiments với logic đã sửa
Generated on: {timestamp}
"""

import subprocess
import os

def run_experiments():
    """Chạy lại experiments với logic đã sửa"""
    
    print("CHAY LAI EXPERIMENTS VOI LOGIC DA SUA")
    print("=" * 50)
    
    # Danh sách experiments để chạy
    experiments = [
        {{
            'name': 'Translation CS->Java',
            'cmd': [
                'py', 'codeattack.py',
                '--attack_model', 'codebert',
                '--victim_model', 'codet5',
                '--task', 'translation',
                '--lang', 'cs_java',
                '--use_ast', '0',
                '--out_dirname', 'test_run_fixed'
            ]
        }},
        {{
            'name': 'Translation Java->CS',
            'cmd': [
                'py', 'codeattack.py',
                '--attack_model', 'codebert',
                '--victim_model', 'codet5',
                '--task', 'translation',
                '--lang', 'java_cs',
                '--use_ast', '0',
                '--out_dirname', 'test_run_fixed'
            ]
        }},
        {{
            'name': 'Code Summarization',
            'cmd': [
                'py', 'codeattack.py',
                '--attack_model', 'codebert',
                '--victim_model', 'codet5',
                '--task', 'summarize',
                '--lang', 'java_en_XX',
                '--use_ast', '0',
                '--out_dirname', 'test_run_fixed'
            ]
        }}
    ]
    
    results = []
    
    for i, exp in enumerate(experiments):
        print(f"\\nExperiment {i+1}: {{exp['name']}}")
        print(f"Command: {{' '.join(exp['cmd'])}}")
        
        try:
            result = subprocess.run(exp['cmd'], capture_output=True, text=True)
            if result.returncode == 0:
                print("Thanh cong")
                results.append({{'name': exp['name'], 'status': 'success'}})
            else:
                print("That bai")
                print(f"Error: {{result.stderr}}")
                results.append({{'name': exp['name'], 'status': 'failed', 'error': result.stderr}})
        except Exception as e:
            print(f"Loi: {{e}}")
            results.append({{'name': exp['name'], 'status': 'error', 'error': str(e)}})
    
    # Lưu kết quả
    with open('experiment_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\\nKET QUA:")
    successful = sum(1 for r in results if r['status'] == 'success')
    print(f"   - Thanh cong: {{successful}}/{{len(results)}}")
    print(f"   - That bai: {{len(results) - successful}}/{{len(results)}}")
    
    return successful == len(results)

if __name__ == "__main__":
    run_experiments()
'''
    
    with open('run_experiments_fixed.py', 'w', encoding='utf-8') as f:
        f.write(run_experiment_script)
    
    print("Da tao script: run_experiments_fixed.py")
    
    # Tạo hướng dẫn tiếp theo
    next_steps = f'''# HUONG DAN TIEP THEO

## SUA DOI DA DUOC AP DUNG THANH CONG!

### Backup duoc tao tai: {backup_dir}

### Cac buoc tiep theo:

1. **Chay lai experiments**:
   ```bash
   py run_experiments_fixed.py
   ```

2. **Hoac chay tung experiment**:
   ```bash
   # Translation CS->Java
   py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang cs_java --use_ast 0 --out_dirname test_run_fixed
   
   # Translation Java->CS  
   py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs --use_ast 0 --out_dirname test_run_fixed
   
   # Code Summarization
   py codeattack.py --attack_model codebert --victim_model codet5 --task summarize --lang java_en_XX --use_ast 0 --out_dirname test_run_fixed
   ```

3. **Kiem tra ket qua**:
   ```bash
   py analyze_results_logic.py
   ```

4. **So sanh voi ket qua cu**:
   - Backup cu: {backup_dir}
   - Ket qua moi: output/translation/codet5/codebert/cs_java_test_run_fixed/

### Metrics can theo doi:

- **Attack Success Rate**: Du kien tang tu 0% len 44.8%
- **Logic Errors**: Du kien giam tu 53.7% xuong 0%
- **BLEU Score Changes**: Kiem tra tinh nhat quan

### Luu y:

- Neu co van de, co the khoi phuc tu backup: {backup_dir}
- Kiem tra ky ket qua truoc khi su dung cho bao cao
- Cap nhat documentation ve logic success moi

### Ho tro:

- Log chi tiet: fix_application_log.json
- Bao cao phan tich: FINAL_ANALYSIS_REPORT.md
- Huong dan su dung: SUCCESS_LOGIC_FIX_GUIDE.md

---
**Ngay ap dung**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Trang thai**: San sang chay experiments
'''
    
    with open('NEXT_STEPS.md', 'w', encoding='utf-8') as f:
        f.write(next_steps)
    
    print("Da tao huong dan: NEXT_STEPS.md")
    
    print(f"\nHOAN THANH!")
    print(f"Sua doi da duoc ap dung thanh cong")
    print(f"Backup duoc tao tai: {backup_dir}")
    print(f"San sang chay lai experiments")
    print(f"Xem huong dan: NEXT_STEPS.md")
    
    return True

if __name__ == "__main__":
    apply_fixes() 