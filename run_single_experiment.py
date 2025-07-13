#!/usr/bin/env python3
"""
Script đơn giản để chạy một experiment cụ thể
"""

import subprocess
import sys
import os

def run_experiment(attack_model, victim_model, task, lang, use_ast=0, use_dfg=0, theta=0.4, input_lang=None):
    """Chạy một experiment cụ thể"""
    
    # Tạo tên thư mục output
    out_dirname = f"{task}_{lang}_{victim_model}_{attack_model}"
    
    # Tạo command
    cmd = f"py codeattack.py --attack_model {attack_model} --victim_model {victim_model} --task {task} --lang {lang} --use_ast {use_ast} --use_dfg {use_dfg} --out_dirname {out_dirname} --theta {theta}"
    
    # Thêm input_lang nếu cần (cho GraphCodeBERT)
    if input_lang:
        cmd += f" --input_lang {input_lang}"
    
    print(f"🚀 Running experiment:")
    print(f"   Attack Model: {attack_model}")
    print(f"   Victim Model: {victim_model}")
    print(f"   Task: {task}")
    print(f"   Language: {lang}")
    print(f"   Output Dir: {out_dirname}")
    print(f"   Command: {cmd}")
    print("="*60)
    
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        print(f"✅ Experiment completed successfully!")
        print(f"📁 Results saved in: output/{out_dirname}/")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Experiment failed with error: {e}")
        return False

def main():
    """Main function với menu đơn giản"""
    
    print("🚀 CodeAttack Single Experiment Runner")
    print("="*50)
    
    # Menu lựa chọn
    print("\n📋 Choose experiment type:")
    print("1. Translation (Java -> C#)")
    print("2. Translation (C# -> Java)")
    print("3. Summarization (Python)")
    print("4. Summarization (Java)")
    print("5. Summarization (PHP)")
    print("6. Refinement (Java Small)")
    print("7. Custom experiment")
    print("0. Exit")
    
    choice = input("\nEnter your choice (0-7): ").strip()
    
    if choice == "0":
        print("👋 Goodbye!")
        return
    
    # Các experiments được định nghĩa sẵn
    experiments = {
        "1": {
            "name": "Translation (Java -> C#)",
            "params": {
                "attack_model": "codebert",
                "victim_model": "codet5",
                "task": "translation",
                "lang": "java_cs_large",
                "use_ast": 0,
                "use_dfg": 0,
                "theta": 0.4
            }
        },
        "2": {
            "name": "Translation (C# -> Java)",
            "params": {
                "attack_model": "codebert",
                "victim_model": "codet5",
                "task": "translation",
                "lang": "cs_java_large",
                "use_ast": 0,
                "use_dfg": 0,
                "theta": 0.4
            }
        },
        "3": {
            "name": "Summarization (Python)",
            "params": {
                "attack_model": "codebert",
                "victim_model": "codet5",
                "task": "summarize",
                "lang": "python_large",
                "use_ast": 0,
                "use_dfg": 0,
                "theta": 0.4
            }
        },
        "4": {
            "name": "Summarization (Java)",
            "params": {
                "attack_model": "codebert",
                "victim_model": "codebert",
                "task": "summarize",
                "lang": "java_large",
                "use_ast": 0,
                "use_dfg": 0,
                "theta": 0.4
            }
        },
        "5": {
            "name": "Summarization (PHP)",
            "params": {
                "attack_model": "codebert",
                "victim_model": "codet5",
                "task": "summarize",
                "lang": "php_large",
                "use_ast": 0,
                "use_dfg": 0,
                "theta": 0.4
            }
        },
        "6": {
            "name": "Refinement (Java Small)",
            "params": {
                "attack_model": "codebert",
                "victim_model": "codet5",
                "task": "refinement",
                "lang": "java_small_large",
                "use_ast": 0,
                "use_dfg": 0,
                "theta": 0.4
            }
        }
    }
    
    if choice in experiments:
        exp = experiments[choice]
        print(f"\n🎯 Running: {exp['name']}")
        
        # Chạy experiment
        success = run_experiment(**exp['params'])
        
        if success:
            print(f"\n✅ {exp['name']} completed successfully!")
        else:
            print(f"\n❌ {exp['name']} failed!")
    
    elif choice == "7":
        # Custom experiment
        print("\n🔧 Custom experiment setup:")
        
        attack_model = input("Attack model (codebert/textfooler/bertattack): ").strip() or "codebert"
        victim_model = input("Victim model (codet5/codebert/graphcodebert/roberta): ").strip() or "codet5"
        task = input("Task (translation/summarize/refinement): ").strip() or "translation"
        lang = input("Language (e.g., java_cs_large, python_large): ").strip() or "java_cs_large"
        theta = float(input("Theta (0.1-0.6): ").strip() or "0.4")
        
        # Thêm input_lang cho GraphCodeBERT
        input_lang = None
        if victim_model == "graphcodebert":
            input_lang = input("Input language (java/c_sharp): ").strip() or "java"
        
        success = run_experiment(
            attack_model=attack_model,
            victim_model=victim_model,
            task=task,
            lang=lang,
            theta=theta,
            input_lang=input_lang
        )
        
        if success:
            print("\n✅ Custom experiment completed successfully!")
        else:
            print("\n❌ Custom experiment failed!")
    
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main() 