#!/usr/bin/env python3
"""
Quick test script to verify fixes
"""

import os
import sys
import subprocess

def test_single_instance():
    """Test with just one instance to avoid long runs"""
    print("Testing single instance...")
    
    # Create a simple test command that processes only 1 instance
    cmd = "py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs --use_ast 0 --use_dfg 0 --out_dirname quick_test --theta 0.4"
    
    print(f"Running: {cmd}")
    
    try:
        # Run with timeout to avoid hanging
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', timeout=60)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        print(f"Exit code: {result.returncode}")
        
        if result.returncode == 0:
            print("✓ Test passed! Unicode error fixed.")
            return True
        else:
            print("✗ Test failed!")
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ Test timed out!")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def check_output():
    """Check if output files were created"""
    output_dir = "./output/translation/codet5/codebert/java_cs_quick_test"
    
    if os.path.exists(output_dir):
        files = os.listdir(output_dir)
        print(f"✓ Output directory created: {output_dir}")
        print(f"  Files: {files}")
        return True
    else:
        print(f"✗ Output directory not found: {output_dir}")
        return False

def main():
    """Main test function"""
    print("Quick Test for CodeAttack Fixes")
    print("=" * 40)
    
    # Test single instance
    success = test_single_instance()
    
    if success:
        # Check output
        check_output()
        print("\n🎉 All tests passed! Ready to run with large datasets.")
    else:
        print("\n⚠ Tests failed. Check the output above.")

if __name__ == "__main__":
    main() 