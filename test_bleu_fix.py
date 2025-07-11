#!/usr/bin/env python3
"""
Test script to verify BLEU fix
"""

import os
import sys
import subprocess

def test_bleu_calculation():
    """Test BLEU calculation with edge cases"""
    print("Testing BLEU calculation...")
    
    # Create test files
    test_dir = "test_bleu"
    os.makedirs(test_dir, exist_ok=True)
    
    # Test case 1: Normal case
    with open(f"{test_dir}/ref1.txt", 'w', encoding='utf-8') as f:
        f.write("hello world\n")
        f.write("good morning\n")
    
    with open(f"{test_dir}/trans1.txt", 'w', encoding='utf-8') as f:
        f.write("hello world\n")
        f.write("good morning\n")
    
    # Test case 2: Empty files
    with open(f"{test_dir}/ref2.txt", 'w', encoding='utf-8') as f:
        pass  # Empty file
    
    with open(f"{test_dir}/trans2.txt", 'w', encoding='utf-8') as f:
        pass  # Empty file
    
    # Test case 3: One empty, one not
    with open(f"{test_dir}/ref3.txt", 'w', encoding='utf-8') as f:
        pass  # Empty file
    
    with open(f"{test_dir}/trans3.txt", 'w', encoding='utf-8') as f:
        f.write("hello world\n")
    
    try:
        # Import and test BLEU function
        sys.path.append('.')
        from bleu import _bleu
        
        print("Testing normal case...")
        score1 = _bleu(f"{test_dir}/ref1.txt", f"{test_dir}/trans1.txt")
        print(f"Normal case BLEU score: {score1}")
        
        print("Testing empty files...")
        score2 = _bleu(f"{test_dir}/ref2.txt", f"{test_dir}/trans2.txt")
        print(f"Empty files BLEU score: {score2}")
        
        print("Testing mixed case...")
        score3 = _bleu(f"{test_dir}/ref3.txt", f"{test_dir}/trans3.txt")
        print(f"Mixed case BLEU score: {score3}")
        
        print("✓ All BLEU tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ BLEU test failed: {e}")
        return False
    finally:
        # Clean up
        import shutil
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)

def test_codeattack_integration():
    """Test CodeAttack with the BLEU fix"""
    print("\nTesting CodeAttack integration...")
    
    # Simple test command
    cmd = "py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs --use_ast 0 --use_dfg 0 --out_dirname bleu_test --theta 0.4"
    
    print(f"Running: {cmd}")
    
    try:
        # Run with timeout
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', timeout=120)
        
        if result.returncode == 0:
            print("✓ CodeAttack test passed!")
            return True
        else:
            print("✗ CodeAttack test failed!")
            if result.stderr:
                print("STDERR:")
                print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("✗ Test timed out!")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Main test function"""
    print("BLEU Fix Test")
    print("=" * 30)
    
    # Test BLEU calculation
    bleu_success = test_bleu_calculation()
    
    # Test CodeAttack integration
    if bleu_success:
        codeattack_success = test_codeattack_integration()
    else:
        codeattack_success = False
    
    # Summary
    print("\n" + "=" * 30)
    print("SUMMARY")
    print("=" * 30)
    
    if bleu_success and codeattack_success:
        print("🎉 All tests passed! BLEU fix is working correctly.")
        print("You can now run CodeAttack with large datasets.")
    else:
        print("⚠ Some tests failed. Check the output above.")
    
    return bleu_success and codeattack_success

if __name__ == "__main__":
    main() 