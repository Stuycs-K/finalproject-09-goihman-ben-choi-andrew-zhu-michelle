#!/usr/bin/env python3

import subprocess
import os
import tempfile
import zipfile

def run_command(command):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Command timed out"

def create_test_wordlist():
    """Create a test wordlist file with the correct password"""
    wordlist_content = """
password
123456
admin
test
password123
qwerty
letmein
welcome
monkey
""".strip()
    
    with open("test_wordlist.txt", "w") as f:
        f.write(wordlist_content)
    print("✓ Created test_wordlist.txt")

def test_wordlist_attack():
    """Test the wordlist attack functionality"""
    print("\n=== Testing Wordlist Attack ===")
    
    returncode, stdout, stderr = run_command("make wordlist ARGS='test.zip test_wordlist.txt'")
    
    if "Password found: password123" in stdout:
        print("✓ Wordlist attack PASSED - Found correct password")
        return True
    else:
        print("✗ Wordlist attack FAILED")
        print(f"Return code: {returncode}")
        print(f"Stdout: {stdout}")
        print(f"Stderr: {stderr}")
        return False

def test_mask_attack_with_wordlist():
    print("\n=== Testing Mask Attack with Wordlist ===")
    
    returncode, stdout, stderr = run_command("make mask ARGS='test.zip test_wordlist.txt password___'")
    
    if "Password found: password123" in stdout:
        print("✓ Mask attack with wordlist PASSED - Found correct password")
        return True
    else:
        print("✗ Mask attack with wordlist FAILED")
        print(f"Return code: {returncode}")
        print(f"Stdout: {stdout}")
        print(f"Stderr: {stderr}")
        return False

def test_mask_brute_force():
    """Test the mask brute force functionality"""
    print("\n=== Testing Mask Brute Force Attack ===")
    
    returncode, stdout, stderr = run_command("make mask ARGS='test.zip password12_'")
    
    if "Password found: password123" in stdout:
        print("✓ Mask brute force PASSED - Found correct password")
        return True
    else:
        print("✗ Mask brute force FAILED (this might timeout for complex masks)")
        print(f"Return code: {returncode}")
        print(f"Stdout: {stdout}")
        print(f"Stderr: {stderr}")
        return False

def test_bomb_detection():
    """Test the bomb detection functionality"""
    print("\n=== Testing Bomb Detection ===")
    
    returncode, stdout, stderr = run_command("make bomb ARGS='test.zip'")
    
    if returncode == 0:
        print("✓ Bomb detection PASSED - Command executed successfully")
        print(f"Output: {stdout.strip()}")
        return True
    else:
        print("✗ Bomb detection FAILED")
        print(f"Return code: {returncode}")
        print(f"Stdout: {stdout}")
        print(f"Stderr: {stderr}")
        return False

def test_error_cases():
    """Test error handling"""
    print("\n=== Testing Error Cases ===")
    
    print("Testing with non-existent zip file...")
    returncode, stdout, stderr = run_command("make wordlist ARGS='nonexistent.zip test_wordlist.txt'")
    
    if "not found" in stdout or returncode != 0:
        print("✓ Error handling PASSED - Correctly handled missing zip file")
    else:
        print("✗ Error handling FAILED - Should have detected missing zip file")
    
    # Test with non-existent wordlist
    print("Testing with non-existent wordlist...")
    returncode, stdout, stderr = run_command("make wordlist ARGS='test.zip nonexistent.txt'")
    
    if "not found" in stdout or returncode != 0:
        print("✓ Error handling PASSED - Correctly handled missing wordlist")
    else:
        print("✗ Error handling FAILED - Should have detected missing wordlist")

def cleanup():
    """Clean up test files"""
    try:
        if os.path.exists("test_wordlist.txt"):
            os.remove("test_wordlist.txt")
            print("✓ Cleaned up test_wordlist.txt")
    except:
        pass

def main():
    """Run all tests"""
    print("=== ZIP CRACKING TOOL TESTS ===")
    print("Testing with test.zip (password: password123)")
    
    # Check if test.zip exists
    if not os.path.exists("test.zip"):
        print("✗ ERROR: test.zip not found in current directory")
        print("Please ensure test.zip exists and has password 'password123'")
        return
    
    create_test_wordlist()
    
    tests_passed = 0
    total_tests = 0
    
    total_tests += 1
    if test_wordlist_attack():
        tests_passed += 1
    
    total_tests += 1
    if test_mask_attack_with_wordlist():
        tests_passed += 1
    
    total_tests += 1
    if test_bomb_detection():
        tests_passed += 1
    
    test_error_cases()
    
    print(f"\n=== TEST SUMMARY ===")
    print(f"Tests passed: {tests_passed}/{total_tests}")
    print(f"Success rate: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_passed == total_tests:
        print("All tests PASSED!")
    else:
        print("Some tests FAILED")
    
    cleanup()

if __name__ == "__main__":
    main()
