#!/usr/bin/env python3
"""
Setup script for CodeAttack on Windows
"""

import os
import sys
import subprocess
import platform

def create_directories():
    """Create necessary directories"""
    dirs = [
        'output',
        'output/translation',
        'output/summarize', 
        'output/refinement',
        'data',
        'data/code_translation',
        'data/code_summarization',
        'data/code_summarization/code-to-text',
        'data/code_summarization/code-to-text/java',
        'data/code_summarization/code-to-text/python',
        'data/code_summarization/code-to-text/php',
        'data/code_summarization/code-to-text/ruby',
        'data/code_summarization/code-to-text/javascript',
        'data/code_summarization/code-to-text/go',
        'data/code_refinement',
        'data/code_refinement/small',
        'data/code_refinement/medium',
        'checkpoints',
        'checkpoints/code_translation',
        'checkpoints/code_translation/codet5',
        'checkpoints/code_translation/codebert',
        'checkpoints/code_translation/graphcodebert',
        'checkpoints/code_translation/plbart',
        'checkpoints/code_summarization',
        'checkpoints/code_summarization/java_en_XX',
        'checkpoints/code_summarization/java_en_XX/codet5',
        'checkpoints/code_summarization/java_en_XX/codebert',
        'checkpoints/code_summarization/java_en_XX/roberta',
        'checkpoints/code_summarization/python_en_XX',
        'checkpoints/code_summarization/python_en_XX/codet5',
        'checkpoints/code_summarization/python_en_XX/codebert',
        'checkpoints/code_summarization/python_en_XX/roberta',
        'checkpoints/code_summarization/php_en_XX',
        'checkpoints/code_summarization/php_en_XX/codet5',
        'checkpoints/code_summarization/php_en_XX/codebert',
        'checkpoints/code_summarization/php_en_XX/roberta',
        'checkpoints/code_summarization/ruby_en_XX',
        'checkpoints/code_summarization/javascript_en_XX',
        'checkpoints/code_summarization/go_en_XX',
        'checkpoints/code_summarization/go_en_XX/codet5',
        'checkpoints/code_refinement',
        'checkpoints/code_refinement/codet5',
        'checkpoints/code_refinement/codebert',
        'checkpoints/code_refinement/graphcodebert'
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created directory: {dir_path}")

def create_sample_data():
    """Create sample data files for testing"""
    
    # Sample translation data
    sample_java = '''public class HelloWorld {
    public static void main(String[] args) {
        System.out.println("Hello, World!");
    }
}'''
    
    sample_cs = '''using System;
public class HelloWorld {
    public static void Main(string[] args) {
        Console.WriteLine("Hello, World!");
    }
}'''
    
    # Create sample translation files
    with open('data/code_translation/test.java-cs.txt.java', 'w') as f:
        f.write(sample_java)
    
    with open('data/code_translation/test.java-cs.txt.cs', 'w') as f:
        f.write(sample_cs)
    
    # Sample summarization data
    sample_summary = {
        "code": sample_java,
        "docstring": "A simple Hello World program in Java"
    }
    
    import json
    with open('data/code_summarization/code-to-text/java/test.jsonl', 'w') as f:
        f.write(json.dumps(sample_summary) + '\n')
    
    # Create sample refinement data
    buggy_code = '''public class Calculator {
    public int add(int a, int b) {
        return a - b;  // Bug: should be a + b
    }
}'''
    
    fixed_code = '''public class Calculator {
    public int add(int a, int b) {
        return a + b;  // Fixed: correct addition
    }
}'''
    
    with open('data/code_refinement/small/test.buggy-fixed.buggy', 'w') as f:
        f.write(buggy_code)
    
    with open('data/code_refinement/small/test.buggy-fixed.fixed', 'w') as f:
        f.write(fixed_code)
    
    print("Created sample data files")

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'torch', 'transformers', 'datasets', 'pandas', 
        'numpy', 'tqdm', 'yaml', 'sklearn', 'tree_sitter'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"✗ {package} - MISSING")
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    return True

def main():
    print("CodeAttack Windows Setup")
    print("=" * 30)
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("Error: Python 3.7 or higher is required")
        sys.exit(1)
    
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.system()} {platform.release()}")
    
    # Create directories
    print("\nCreating directories...")
    create_directories()
    
    # Create sample data
    print("\nCreating sample data...")
    create_sample_data()
    
    # Check dependencies
    print("\nChecking dependencies...")
    if check_dependencies():
        print("\n✓ Setup completed successfully!")
        print("\nYou can now run CodeAttack with:")
        print("python codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs --use_ast 0 --use_dfg 0 --out_dirname test_run --theta 0.4")
    else:
        print("\n✗ Setup incomplete. Please install missing dependencies.")
        sys.exit(1)

if __name__ == "__main__":
    main() 