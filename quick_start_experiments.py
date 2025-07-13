#!/usr/bin/env python3
"""
Script đơn giản để bắt đầu chạy experiments theo báo cáo
"""

import subprocess
import os
import sys
import time
from typing import List, Dict

def run_command(command: str, description: str = "") -> bool:
    """Chạy một lệnh và trả về True nếu thành công"""
    print(f"\n{'='*60}")
    print(f"🚀 {description}")
    print(f"📝 Command: {command}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Success: {description}")
        if result.stdout:
            print(f"Output: {result.stdout[:500]}...")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {description}")
        print(f"Error: {e.stderr}")
        return False

def check_environment() -> bool:
    """Kiểm tra môi trường trước khi chạy"""
    print("🔍 Checking environment...")
    
    # Kiểm tra Python
    if not run_command("python --version", "Check Python version"):
        return False
    
    # Kiểm tra thư mục cần thiết
    required_dirs = ['data', 'configs', 'checkpoints']
    for dir_name in required_dirs:
        if not os.path.exists(dir_name):
            print(f"❌ Missing directory: {dir_name}")
            return False
        print(f"✅ Found directory: {dir_name}")
    
    # Kiểm tra file chính
    if not os.path.exists('codeattack.py'):
        print("❌ Missing main file: codeattack.py")
        return False
    print("✅ Found main file: codeattack.py")
    
    return True

def run_basic_experiments() -> None:
    """Chạy các experiments cơ bản để test"""
    print("\n🎯 Running basic experiments...")
    
    # Test 1: Translation với CodeT5
    run_command(
        "py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs --use_ast 0 --use_dfg 0 --out_dirname test_translation_codet5 --theta 0.4",
        "Test Translation with CodeT5"
    )
    
    # Test 2: Summarization với CodeBERT
    run_command(
        "py codeattack.py --attack_model codebert --victim_model codebert --task summarize --lang java --use_ast 0 --use_dfg 0 --out_dirname test_summarize_codebert --theta 0.4",
        "Test Summarization with CodeBERT"
    )
    
    # Test 3: Refinement với GraphCodeBERT
    run_command(
        "py codeattack.py --attack_model codebert --victim_model graphcodebert --task refinement --lang java_small --use_ast 0 --use_dfg 0 --out_dirname test_refinement_graphcodebert --input_lang java --theta 0.4",
        "Test Refinement with GraphCodeBERT"
    )

def run_rq1_experiments() -> None:
    """Chạy experiments cho RQ1 - Transferability"""
    print("\n🎯 Running RQ1 - Transferability experiments...")
    
    experiments = [
        # Translation experiments
        {
            "cmd": "py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --out_dirname rq1_translation_java_cs_codet5 --theta 0.4",
            "desc": "RQ1: Java->C# Translation with CodeT5"
        },
        {
            "cmd": "py codeattack.py --attack_model codebert --victim_model codebert --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --out_dirname rq1_translation_java_cs_codebert --theta 0.4",
            "desc": "RQ1: Java->C# Translation with CodeBERT"
        },
        {
            "cmd": "py codeattack.py --attack_model codebert --victim_model graphcodebert --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --out_dirname rq1_translation_java_cs_graphcodebert --input_lang java --theta 0.4",
            "desc": "RQ1: Java->C# Translation with GraphCodeBERT"
        },
        
        # Summarization experiments
        {
            "cmd": "py codeattack.py --attack_model codebert --victim_model codet5 --task summarize --lang python_large --use_ast 0 --use_dfg 0 --out_dirname rq1_summarize_python_codet5 --theta 0.4",
            "desc": "RQ1: Python Summarization with CodeT5"
        },
        {
            "cmd": "py codeattack.py --attack_model codebert --victim_model codebert --task summarize --lang java_large --use_ast 0 --use_dfg 0 --out_dirname rq1_summarize_java_codebert --theta 0.4",
            "desc": "RQ1: Java Summarization with CodeBERT"
        },
        
        # Refinement experiments
        {
            "cmd": "py codeattack.py --attack_model codebert --victim_model codet5 --task refinement --lang java_small_large --use_ast 0 --use_dfg 0 --out_dirname rq1_refinement_java_small_codet5 --theta 0.4",
            "desc": "RQ1: Java Small Refinement with CodeT5"
        }
    ]
    
    for i, exp in enumerate(experiments, 1):
        print(f"\n📊 Experiment {i}/{len(experiments)}")
        run_command(exp["cmd"], exp["desc"])
        time.sleep(2)  # Nghỉ giữa các experiments

def run_rq2_experiments() -> None:
    """Chạy experiments cho RQ2 - Quality comparison"""
    print("\n🎯 Running RQ2 - Quality comparison experiments...")
    
    experiments = [
        {
            "cmd": "py codeattack.py --attack_model textfooler --victim_model codet5 --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --out_dirname rq2_textfooler_java_cs_codet5 --theta 0.4",
            "desc": "RQ2: TextFooler vs CodeT5"
        },
        {
            "cmd": "py codeattack.py --attack_model bertattack --victim_model codet5 --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --out_dirname rq2_bertattack_java_cs_codet5 --theta 0.4",
            "desc": "RQ2: BERT-Attack vs CodeT5"
        }
    ]
    
    for i, exp in enumerate(experiments, 1):
        print(f"\n📊 Experiment {i}/{len(experiments)}")
        run_command(exp["cmd"], exp["desc"])
        time.sleep(2)

def run_rq3_experiments() -> None:
    """Chạy experiments cho RQ3 - Change limits"""
    print("\n🎯 Running RQ3 - Change limit experiments...")
    
    thetas = [0.1, 0.2, 0.4, 0.6]
    
    for theta in thetas:
        cmd = f"py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --out_dirname rq3_change_limit_{int(theta*100)} --theta {theta}"
        desc = f"RQ3: Change limit {int(theta*100)}%"
        run_command(cmd, desc)
        time.sleep(2)

def run_rq4_experiments() -> None:
    """Chạy experiments cho RQ4 - Component analysis"""
    print("\n🎯 Running RQ4 - Component analysis experiments...")
    
    experiments = [
        {
            "cmd": "py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --use_imp 1 --out_dirname rq4_important_words --theta 0.4",
            "desc": "RQ4: Important words selection"
        },
        {
            "cmd": "py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --use_imp 0 --out_dirname rq4_random_words --theta 0.4",
            "desc": "RQ4: Random words selection"
        }
    ]
    
    for i, exp in enumerate(experiments, 1):
        print(f"\n📊 Experiment {i}/{len(experiments)}")
        run_command(exp["cmd"], exp["desc"])
        time.sleep(2)

def main():
    """Main function"""
    print("🚀 CodeAttack Experiments Runner")
    print("="*60)
    
    # Kiểm tra môi trường
    if not check_environment():
        print("❌ Environment check failed. Please fix the issues above.")
        return
    
    print("\n✅ Environment check passed!")
    
    # Menu lựa chọn
    while True:
        print("\n" + "="*60)
        print("📋 Choose experiments to run:")
        print("1. Basic experiments (quick test)")
        print("2. RQ1 - Transferability experiments")
        print("3. RQ2 - Quality comparison experiments")
        print("4. RQ3 - Change limit experiments")
        print("5. RQ4 - Component analysis experiments")
        print("6. Run all experiments")
        print("0. Exit")
        print("="*60)
        
        choice = input("Enter your choice (0-6): ").strip()
        
        if choice == "0":
            print("👋 Goodbye!")
            break
        elif choice == "1":
            run_basic_experiments()
        elif choice == "2":
            run_rq1_experiments()
        elif choice == "3":
            run_rq2_experiments()
        elif choice == "4":
            run_rq3_experiments()
        elif choice == "5":
            run_rq4_experiments()
        elif choice == "6":
            print("🎯 Running all experiments...")
            run_basic_experiments()
            run_rq1_experiments()
            run_rq2_experiments()
            run_rq3_experiments()
            run_rq4_experiments()
            print("✅ All experiments completed!")
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 