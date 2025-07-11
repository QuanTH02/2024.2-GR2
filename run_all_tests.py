#!/usr/bin/env python3
"""
Run all tests systematically to ensure everything works
"""

import os
import sys
import subprocess
import time

def run_test(test_name, test_script, timeout=120):
    """Run a single test"""
    print(f"\n{'='*20} {test_name} {'='*20}")
    
    try:
        start_time = time.time()
        result = subprocess.run([sys.executable, test_script], 
                              capture_output=True, text=True, encoding='utf-8', timeout=timeout)
        end_time = time.time()
        
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"✓ {test_name} PASSED ({duration:.2f}s)")
            return True, duration
        else:
            print(f"✗ {test_name} FAILED ({duration:.2f}s)")
            if result.stderr:
                print("STDERR:")
                print(result.stderr[-300:])  # Show last 300 chars
            return False, duration
            
    except subprocess.TimeoutExpired:
        print(f"✗ {test_name} TIMEOUT")
        return False, timeout
    except Exception as e:
        print(f"✗ {test_name} ERROR: {e}")
        return False, 0

def check_prerequisites():
    """Check if all required files exist"""
    print("Checking prerequisites...")
    
    required_files = [
        "data/code_translation/test.java-cs.txt.java",
        "data/code_translation/large.java-cs.txt.java",
        "data/code_summarization/code-to-text/java/test.jsonl",
        "data/code_summarization/code-to-text/java/large.jsonl",
        "configs/config_data.yaml",
        "attack.py",
        "bleu.py",
        "codeattack.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✓ {file_path}")
    
    if missing_files:
        print(f"\n❌ Missing files: {missing_files}")
        print("Please run the dataset creation scripts first:")
        print("1. py expand_test_data.py")
        print("2. py create_large_test_dataset.py")
        return False
    
    print("✓ All prerequisites met!")
    return True

def main():
    """Main function to run all tests"""
    print("CodeAttack Comprehensive Test Suite")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        return False
    
    # Define all tests
    tests = [
        ("BLEU Edge Cases", "test_bleu_edge_cases.py", 60),
        ("BLEU Fix", "test_bleu_fix.py", 60),
        ("Quick Test", "quick_test.py", 120),
        ("Demo Large Dataset", "demo_large_dataset.py", 30),
        ("Final Test", "final_test.py", 300)
    ]
    
    results = []
    
    # Run each test
    for test_name, test_script, timeout in tests:
        if os.path.exists(test_script):
            success, duration = run_test(test_name, test_script, timeout)
            results.append({
                "name": test_name,
                "success": success,
                "duration": duration
            })
        else:
            print(f"⚠ {test_script} not found, skipping {test_name}")
            results.append({
                "name": test_name,
                "success": False,
                "duration": 0
            })
    
    # Summary
    print("\n" + "=" * 50)
    print("FINAL SUMMARY")
    print("=" * 50)
    
    successful = sum(1 for r in results if r['success'])
    total = len(results)
    total_duration = sum(r['duration'] for r in results)
    
    for result in results:
        status = "✓ PASS" if result['success'] else "✗ FAIL"
        print(f"{result['name']}: {status} ({result['duration']:.2f}s)")
    
    print(f"\nOverall: {successful}/{total} tests passed")
    print(f"Total time: {total_duration:.2f} seconds")
    
    if successful == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ CodeAttack is fully functional")
        print("✅ All technical issues resolved")
        print("✅ Ready for production use")
        
        print("\n🚀 You can now run:")
        print("• Small datasets: --lang java_cs")
        print("• Large datasets: --lang java_cs_large")
        print("• Different tasks: summarize, refinement")
        print("• Different models: codebert, bertattack, textfooler")
        
    elif successful >= total * 0.8:  # 80% success rate
        print("\n⚠ Most tests passed, but some issues remain.")
        print("Check the failed tests above for details.")
        
    else:
        print("\n❌ Many tests failed.")
        print("Please check the errors above and fix them.")
    
    return successful == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 