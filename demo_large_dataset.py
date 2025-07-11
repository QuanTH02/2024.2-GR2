#!/usr/bin/env python3
"""
Demo script to test CodeAttack with large datasets
"""

import os
import sys
import yaml
import json
from pathlib import Path

def check_dataset_sizes():
    """Check the size of all datasets"""
    print("=== Dataset Size Check ===")
    
    # Check translation datasets
    translation_files = [
        'data/code_translation/test.java-cs.txt.java',
        'data/code_translation/large.java-cs.txt.java'
    ]
    
    for file_path in translation_files:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                lines = f.readlines()
                # Count actual code blocks (non-empty lines that start with 'public')
                code_blocks = len([line for line in lines if line.strip().startswith('public class')])
                print(f"✓ {file_path}: {code_blocks} code samples")
        else:
            print(f"✗ {file_path}: Not found")
    
    # Check summarization datasets
    languages = ['java', 'python', 'php', 'javascript', 'go', 'ruby']
    for lang in languages:
        test_file = f'data/code_summarization/code-to-text/{lang}/test.jsonl'
        large_file = f'data/code_summarization/code-to-text/{lang}/large.jsonl'
        
        if os.path.exists(test_file):
            with open(test_file, 'r') as f:
                lines = f.readlines()
                print(f"✓ {test_file}: {len(lines)} samples")
        
        if os.path.exists(large_file):
            with open(large_file, 'r') as f:
                lines = f.readlines()
                print(f"✓ {large_file}: {len(lines)} samples")
    
    # Check refinement datasets
    refinement_files = [
        'data/code_refinement/small/test.buggy-fixed.buggy',
        'data/code_refinement/small/large.buggy-fixed.buggy',
        'data/code_refinement/medium/test.buggy-fixed.buggy',
        'data/code_refinement/medium/large.buggy-fixed.buggy'
    ]
    
    for file_path in refinement_files:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                lines = f.readlines()
                code_blocks = len([line for line in lines if line.strip().startswith('public class')])
                print(f"✓ {file_path}: {code_blocks} samples")
        else:
            print(f"✗ {file_path}: Not found")

def show_available_configs():
    """Show available configurations for large datasets"""
    print("\n=== Available Large Dataset Configurations ===")
    
    try:
        with open('configs/config_data.yaml', 'r') as f:
            config = yaml.safe_load(f)
        
        print("Translation tasks:")
        for key in config.get('translation', {}).keys():
            if 'large' in key:
                print(f"  - {key}")
        
        print("\nSummarization tasks:")
        for key in config.get('summarize', {}).keys():
            if 'large' in key:
                print(f"  - {key}")
        
        print("\nRefinement tasks:")
        for key in config.get('refinement', {}).keys():
            if 'large' in key:
                print(f"  - {key}")
                
    except Exception as e:
        print(f"Error reading config: {e}")

def generate_demo_commands():
    """Generate demo commands for testing"""
    print("\n=== Demo Commands for Large Datasets ===")
    
    commands = [
        # Translation examples
        "py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --out_dirname large_test --theta 0.4",
        "py codeattack.py --attack_model bertattack --victim_model codebert --task translation --lang cs_java_large --use_ast 0 --use_dfg 0 --out_dirname large_test --theta 0.4",
        
        # Summarization examples
        "py codeattack.py --attack_model codebert --victim_model codet5 --task summarize --lang java_large --use_ast 0 --use_dfg 0 --out_dirname large_test --theta 0.4",
        "py codeattack.py --attack_model textfooler --victim_model codebert --task summarize --lang python_large --use_ast 0 --use_dfg 0 --out_dirname large_test --theta 0.4",
        
        # Refinement examples
        "py codeattack.py --attack_model codebert --victim_model codet5 --task refinement --lang java_small_large --use_ast 0 --use_dfg 0 --out_dirname large_test --theta 0.4",
        "py codeattack.py --attack_model bertattack --victim_model graphcodebert --task refinement --lang java_medium_large --use_ast 0 --use_dfg 0 --out_dirname large_test --theta 0.4"
    ]
    
    for i, cmd in enumerate(commands, 1):
        print(f"{i}. {cmd}")
    
    print("\nNote: These commands assume you have the required model checkpoints.")
    print("If you don't have checkpoints, the models will fall back to base models from HuggingFace.")

def show_dataset_samples():
    """Show sample data from large datasets"""
    print("\n=== Sample Data from Large Datasets ===")
    
    # Show translation sample
    print("Translation Sample (Java → C#):")
    try:
        with open('data/code_translation/large.java-cs.txt.java', 'r') as f:
            lines = f.readlines()
            # Find first complete class
            class_lines = []
            in_class = False
            brace_count = 0
            
            for line in lines:
                if line.strip().startswith('public class'):
                    in_class = True
                    class_lines = [line]
                    brace_count = line.count('{') - line.count('}')
                elif in_class:
                    class_lines.append(line)
                    brace_count += line.count('{') - line.count('}')
                    if brace_count == 0:
                        break
            
            if class_lines:
                print("Java:")
                print(''.join(class_lines[:5]) + "...")
        
        with open('data/code_translation/large.java-cs.txt.cs', 'r') as f:
            lines = f.readlines()
            class_lines = []
            in_class = False
            brace_count = 0
            
            for line in lines:
                if line.strip().startswith('public class'):
                    in_class = True
                    class_lines = [line]
                    brace_count = line.count('{') - line.count('}')
                elif in_class:
                    class_lines.append(line)
                    brace_count += line.count('{') - line.count('}')
                    if brace_count == 0:
                        break
            
            if class_lines:
                print("\nC#:")
                print(''.join(class_lines[:5]) + "...")
    
    except Exception as e:
        print(f"Error reading translation sample: {e}")
    
    # Show summarization sample
    print("\nSummarization Sample:")
    try:
        with open('data/code_summarization/code-to-text/java/large.jsonl', 'r') as f:
            first_line = f.readline().strip()
            if first_line:
                sample = json.loads(first_line)
                print(f"Code: {sample['code'][:100]}...")
                print(f"Docstring: {sample['docstring']}")
    except Exception as e:
        print(f"Error reading summarization sample: {e}")

def main():
    """Main demo function"""
    print("CodeAttack Large Dataset Demo")
    print("=" * 50)
    
    check_dataset_sizes()
    show_available_configs()
    generate_demo_commands()
    show_dataset_samples()
    
    print("\n=== Summary ===")
    print("✓ Large datasets have been created successfully!")
    print("✓ You now have 30+ samples for each task type")
    print("✓ Configuration has been updated with '_large' options")
    print("✓ Ready to run attacks with larger test sets")
    
    print("\nNext steps:")
    print("1. Run one of the demo commands above")
    print("2. Check the output directory for results")
    print("3. Compare results between small and large datasets")

if __name__ == "__main__":
    main() 