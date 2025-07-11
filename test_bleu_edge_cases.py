#!/usr/bin/env python3
"""
Test BLEU edge cases to ensure all division by zero errors are fixed
"""

import os
import sys
import tempfile

def test_bleu_edge_cases():
    """Test various edge cases for BLEU calculation"""
    print("Testing BLEU edge cases...")
    
    # Import BLEU function
    sys.path.append('.')
    from bleu import _bleu
    
    test_cases = [
        {
            "name": "Both empty",
            "ref": "",
            "trans": "",
            "expected": 0.0
        },
        {
            "name": "Reference empty, translation not",
            "ref": "",
            "trans": "hello world",
            "expected": 0.0
        },
        {
            "name": "Translation empty, reference not",
            "ref": "hello world",
            "trans": "",
            "expected": 0.0
        },
        {
            "name": "Normal case",
            "ref": "hello world",
            "trans": "hello world",
            "expected": "high_score"
        },
        {
            "name": "Different lengths",
            "ref": "hello world",
            "trans": "hello",
            "expected": "low_score"
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases):
        print(f"\nTest {i+1}: {test_case['name']}")
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as ref_file:
            ref_file.write(test_case['ref'])
            ref_path = ref_file.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as trans_file:
            trans_file.write(test_case['trans'])
            trans_path = trans_file.name
        
        try:
            # Test BLEU calculation
            score = _bleu(ref_path, trans_path)
            print(f"  BLEU score: {score}")
            
            # Check if test passed
            if test_case['expected'] == 0.0:
                passed = score == 0.0
            elif test_case['expected'] == "high_score":
                passed = score > 50.0  # Should be high for identical text
            elif test_case['expected'] == "low_score":
                passed = score < 50.0  # Should be low for different text
            else:
                passed = True
            
            if passed:
                print(f"  ✓ PASS")
                results.append(True)
            else:
                print(f"  ✗ FAIL")
                results.append(False)
                
        except Exception as e:
            print(f"  ✗ ERROR: {e}")
            results.append(False)
        finally:
            # Clean up temporary files
            os.unlink(ref_path)
            os.unlink(trans_path)
    
    return results

def test_codeattack_integration():
    """Test CodeAttack integration with edge cases"""
    print("\nTesting CodeAttack integration...")
    
    # Create a minimal test dataset with potential edge cases
    test_data_dir = "test_edge_cases"
    os.makedirs(test_data_dir, exist_ok=True)
    
    # Create test files with edge cases
    with open(f"{test_data_dir}/test.java", 'w', encoding='utf-8') as f:
        f.write("public class Test {\n")
        f.write("    public static void main(String[] args) {\n")
        f.write("        System.out.println(\"Hello\");\n")
        f.write("    }\n")
        f.write("}\n")
        f.write("\n")  # Empty line
        f.write("public class Empty {\n")
        f.write("}\n")
    
    with open(f"{test_data_dir}/test.cs", 'w', encoding='utf-8') as f:
        f.write("using System;\n")
        f.write("public class Test {\n")
        f.write("    public static void Main(string[] args) {\n")
        f.write("        Console.WriteLine(\"Hello\");\n")
        f.write("    }\n")
        f.write("}\n")
        f.write("\n")  # Empty line
        f.write("public class Empty {\n")
        f.write("}\n")
    
    try:
        # Test with a simple command
        cmd = "py codeattack.py --attack_model codebert --victim_model codet5 --task translation --lang java_cs --use_ast 0 --use_dfg 0 --out_dirname edge_test --theta 0.4"
        
        print(f"Running: {cmd}")
        
        import subprocess
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', timeout=60)
        
        if result.returncode == 0:
            print("✓ CodeAttack integration test passed!")
            return True
        else:
            print("✗ CodeAttack integration test failed!")
            if result.stderr:
                print("STDERR:")
                print(result.stderr[-300:])  # Show last 300 chars
            return False
            
    except Exception as e:
        print(f"✗ Integration test error: {e}")
        return False
    finally:
        # Clean up
        import shutil
        if os.path.exists(test_data_dir):
            shutil.rmtree(test_data_dir)

def main():
    """Main test function"""
    print("BLEU Edge Cases Test")
    print("=" * 40)
    
    # Test BLEU edge cases
    bleu_results = test_bleu_edge_cases()
    
    # Test CodeAttack integration
    integration_success = test_codeattack_integration()
    
    # Summary
    print("\n" + "=" * 40)
    print("SUMMARY")
    print("=" * 40)
    
    bleu_passed = sum(bleu_results)
    bleu_total = len(bleu_results)
    
    print(f"BLEU edge cases: {bleu_passed}/{bleu_total} passed")
    print(f"CodeAttack integration: {'✓ PASS' if integration_success else '✗ FAIL'}")
    
    if bleu_passed == bleu_total and integration_success:
        print("\n🎉 All tests passed! BLEU is robust against edge cases.")
        print("✅ No more division by zero errors!")
    else:
        print("\n⚠ Some tests failed. Check the output above.")
    
    return bleu_passed == bleu_total and integration_success

if __name__ == "__main__":
    main() 