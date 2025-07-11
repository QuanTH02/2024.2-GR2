#!/usr/bin/env python3
"""
Script to test CodeAttack with large datasets
"""

import os
import sys
import subprocess
import time

def run_attack_command(cmd):
    """Run attack command and handle errors"""
    print(f"Running: {cmd}")
    print("=" * 80)
    
    try:
        # Run the command
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
        
        # Print output
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"Exit code: {result.returncode}")
        
        if result.returncode == 0:
            print("✓ Command completed successfully!")
        else:
            print("✗ Command failed!")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running command: {e}")
        return False

def test_small_vs_large():
    """Test small vs large datasets"""
    print("Testing Small vs Large Datasets")
    print("=" * 50)
    
    # Test commands
    test_commands = [
        # Small dataset test
        {
            "name": "Small Dataset (5 samples)",
            "cmd": "py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs --use_ast 0 --use_dfg 0 --out_dirname small_test --theta 0.4"
        },
        # Large dataset test  
        {
            "name": "Large Dataset (30 samples)",
            "cmd": "py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --out_dirname large_test --theta 0.4"
        }
    ]
    
    results = []
    
    for test in test_commands:
        print(f"\n{test['name']}")
        print("-" * 30)
        
        start_time = time.time()
        success = run_attack_command(test['cmd'])
        end_time = time.time()
        
        duration = end_time - start_time
        
        results.append({
            "name": test['name'],
            "success": success,
            "duration": duration
        })
        
        print(f"Duration: {duration:.2f} seconds")
        
        # Wait a bit between tests
        time.sleep(2)
    
    # Summary
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    for result in results:
        status = "✓ PASS" if result['success'] else "✗ FAIL"
        print(f"{result['name']}: {status} ({result['duration']:.2f}s)")
    
    return results

def test_different_tasks():
    """Test different tasks with large datasets"""
    print("\nTesting Different Tasks with Large Datasets")
    print("=" * 50)
    
    task_commands = [
        {
            "name": "Translation (Java → C#)",
            "cmd": "py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs_large --use_ast 0 --use_dfg 0 --out_dirname large_translation --theta 0.4"
        },
        {
            "name": "Summarization (Java)",
            "cmd": "py codeattack.py --attack_model codebert --victim_model codet5 --task summarize --lang java_large --use_ast 0 --use_dfg 0 --out_dirname large_summarization --theta 0.4"
        },
        {
            "name": "Refinement (Java Small)",
            "cmd": "py codeattack.py --attack_model codebert --victim_model codet5 --task refinement --lang java_small_large --use_ast 0 --use_dfg 0 --out_dirname large_refinement --theta 0.4"
        }
    ]
    
    results = []
    
    for task in task_commands:
        print(f"\n{task['name']}")
        print("-" * 30)
        
        start_time = time.time()
        success = run_attack_command(task['cmd'])
        end_time = time.time()
        
        duration = end_time - start_time
        
        results.append({
            "name": task['name'],
            "success": success,
            "duration": duration
        })
        
        print(f"Duration: {duration:.2f} seconds")
        
        # Wait between tasks
        time.sleep(3)
    
    return results

def check_output_files():
    """Check output files generated"""
    print("\nChecking Output Files")
    print("=" * 30)
    
    output_dirs = [
        "./output/translation/codet5/codebert/java_cs_small_test",
        "./output/translation/codet5/codebert/java_cs_large_test",
        "./output/translation/codet5/codebert/java_cs_large_translation",
        "./output/summarize/codet5/codebert/java_large_summarization",
        "./output/refinement/codet5/codebert/java_small_large_refinement"
    ]
    
    for output_dir in output_dirs:
        if os.path.exists(output_dir):
            files = os.listdir(output_dir)
            print(f"✓ {output_dir}: {len(files)} files")
            
            # Show some sample files
            json_files = [f for f in files if f.endswith('.json')]
            if json_files:
                print(f"  JSON files: {json_files[:3]}...")
        else:
            print(f"✗ {output_dir}: Not found")

def main():
    """Main function"""
    print("CodeAttack Large Dataset Testing")
    print("=" * 50)
    
    # Check if datasets exist
    print("Checking datasets...")
    
    required_files = [
        "data/code_translation/test.java-cs.txt.java",
        "data/code_translation/large.java-cs.txt.java",
        "data/code_summarization/code-to-text/java/test.jsonl",
        "data/code_summarization/code-to-text/java/large.jsonl"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - Missing!")
            return
    
    print("\nAll required files found!")
    
    # Run tests
    print("\nStarting tests...")
    
    # Test small vs large
    small_large_results = test_small_vs_large()
    
    # Test different tasks
    task_results = test_different_tasks()
    
    # Check outputs
    check_output_files()
    
    # Final summary
    print("\n" + "=" * 50)
    print("FINAL SUMMARY")
    print("=" * 50)
    
    all_results = small_large_results + task_results
    
    successful = sum(1 for r in all_results if r['success'])
    total = len(all_results)
    
    print(f"Tests completed: {successful}/{total} successful")
    
    if successful == total:
        print("🎉 All tests passed! Large datasets are working correctly.")
    else:
        print("⚠ Some tests failed. Check the output above for details.")
    
    print("\nNext steps:")
    print("1. Check the output directories for results")
    print("2. Compare performance between small and large datasets")
    print("3. Analyze attack success rates and BLEU scores")

if __name__ == "__main__":
    main() 