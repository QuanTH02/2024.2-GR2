#!/usr/bin/env python3
"""
Script to expand test data with more samples for CodeAttack evaluation
"""

import os
import json
import random

def create_expanded_translation_data():
    """Create more translation test samples"""
    
    # Java to C# translation samples
    java_samples = [
        '''public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }
    
    public int subtract(int a, int b) {
        return a - b;
    }
}''',
        '''public class StringUtils {
    public static String reverse(String str) {
        if (str == null) return null;
        return new StringBuilder(str).reverse().toString();
    }
    
    public static boolean isEmpty(String str) {
        return str == null || str.length() == 0;
    }
}''',
        '''public class ArrayHelper {
    public static int[] sort(int[] arr) {
        if (arr == null) return null;
        Arrays.sort(arr);
        return arr;
    }
    
    public static int findMax(int[] arr) {
        if (arr == null || arr.length == 0) return -1;
        return Arrays.stream(arr).max().getAsInt();
    }
}''',
        '''public class FileHandler {
    public static void writeToFile(String filename, String content) {
        try (FileWriter writer = new FileWriter(filename)) {
            writer.write(content);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public static String readFromFile(String filename) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            return reader.lines().collect(Collectors.joining("\\n"));
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }
}''',
        '''public class MathUtils {
    public static double power(double base, double exponent) {
        return Math.pow(base, exponent);
    }
    
    public static int factorial(int n) {
        if (n <= 1) return 1;
        return n * factorial(n - 1);
    }
    
    public static boolean isPrime(int n) {
        if (n < 2) return false;
        for (int i = 2; i <= Math.sqrt(n); i++) {
            if (n % i == 0) return false;
        }
        return true;
    }
}'''
    ]
    
    cs_samples = [
        '''using System;

public class Calculator {
    public int Add(int a, int b) {
        return a + b;
    }
    
    public int Subtract(int a, int b) {
        return a - b;
    }
}''',
        '''using System;
using System.Text;

public class StringUtils {
    public static string Reverse(string str) {
        if (str == null) return null;
        char[] charArray = str.ToCharArray();
        Array.Reverse(charArray);
        return new string(charArray);
    }
    
    public static bool IsEmpty(string str) {
        return string.IsNullOrEmpty(str);
    }
}''',
        '''using System;
using System.Linq;

public class ArrayHelper {
    public static int[] Sort(int[] arr) {
        if (arr == null) return null;
        Array.Sort(arr);
        return arr;
    }
    
    public static int FindMax(int[] arr) {
        if (arr == null || arr.Length == 0) return -1;
        return arr.Max();
    }
}''',
        '''using System;
using System.IO;

public class FileHandler {
    public static void WriteToFile(string filename, string content) {
        try {
            File.WriteAllText(filename, content);
        } catch (IOException e) {
            Console.WriteLine(e.Message);
        }
    }
    
    public static string ReadFromFile(string filename) {
        try {
            return File.ReadAllText(filename);
        } catch (IOException e) {
            Console.WriteLine(e.Message);
            return null;
        }
    }
}''',
        '''using System;

public class MathUtils {
    public static double Power(double base, double exponent) {
        return Math.Pow(base, exponent);
    }
    
    public static int Factorial(int n) {
        if (n <= 1) return 1;
        return n * Factorial(n - 1);
    }
    
    public static bool IsPrime(int n) {
        if (n < 2) return false;
        for (int i = 2; i <= Math.Sqrt(n); i++) {
            if (n % i == 0) return false;
        }
        return true;
    }
}'''
    ]
    
    # Write expanded translation data
    with open('data/code_translation/test.java-cs.txt.java', 'w') as f:
        for sample in java_samples:
            f.write(sample + '\n')
    
    with open('data/code_translation/test.java-cs.txt.cs', 'w') as f:
        for sample in cs_samples:
            f.write(sample + '\n')
    
    print(f"✓ Created {len(java_samples)} translation samples")

def create_expanded_summarization_data():
    """Create more summarization test samples"""
    
    summarization_samples = [
        {
            "code": '''public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }
    
    public int subtract(int a, int b) {
        return a - b;
    }
    
    public int multiply(int a, int b) {
        return a * b;
    }
    
    public double divide(int a, int b) {
        if (b == 0) throw new ArithmeticException("Division by zero");
        return (double) a / b;
    }
}''',
            "docstring": "A simple calculator class with basic arithmetic operations including addition, subtraction, multiplication, and division with error handling for division by zero."
        },
        {
            "code": '''public class StringUtils {
    public static String reverse(String str) {
        if (str == null) return null;
        return new StringBuilder(str).reverse().toString();
    }
    
    public static boolean isEmpty(String str) {
        return str == null || str.length() == 0;
    }
    
    public static String toUpperCase(String str) {
        return str != null ? str.toUpperCase() : null;
    }
    
    public static int countWords(String str) {
        if (isEmpty(str)) return 0;
        return str.trim().split("\\s+").length;
    }
}''',
            "docstring": "Utility class for string operations including reverse, empty check, case conversion, and word counting functionality."
        },
        {
            "code": '''public class ArrayHelper {
    public static int[] sort(int[] arr) {
        if (arr == null) return null;
        Arrays.sort(arr);
        return arr;
    }
    
    public static int findMax(int[] arr) {
        if (arr == null || arr.length == 0) return -1;
        return Arrays.stream(arr).max().getAsInt();
    }
    
    public static int findMin(int[] arr) {
        if (arr == null || arr.length == 0) return -1;
        return Arrays.stream(arr).min().getAsInt();
    }
    
    public static double average(int[] arr) {
        if (arr == null || arr.length == 0) return 0.0;
        return Arrays.stream(arr).average().orElse(0.0);
    }
}''',
            "docstring": "Helper class for array operations including sorting, finding maximum and minimum values, and calculating average of array elements."
        },
        {
            "code": '''public class FileHandler {
    public static void writeToFile(String filename, String content) {
        try (FileWriter writer = new FileWriter(filename)) {
            writer.write(content);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public static String readFromFile(String filename) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            return reader.lines().collect(Collectors.joining("\\n"));
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }
    
    public static boolean fileExists(String filename) {
        return new File(filename).exists();
    }
    
    public static long getFileSize(String filename) {
        File file = new File(filename);
        return file.exists() ? file.length() : -1;
    }
}''',
            "docstring": "File handling utility class with methods for writing to files, reading from files, checking file existence, and getting file size."
        },
        {
            "code": '''public class MathUtils {
    public static double power(double base, double exponent) {
        return Math.pow(base, exponent);
    }
    
    public static int factorial(int n) {
        if (n <= 1) return 1;
        return n * factorial(n - 1);
    }
    
    public static boolean isPrime(int n) {
        if (n < 2) return false;
        for (int i = 2; i <= Math.sqrt(n); i++) {
            if (n % i == 0) return false;
        }
        return true;
    }
    
    public static int gcd(int a, int b) {
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }
}''',
            "docstring": "Mathematical utility class providing functions for power calculation, factorial computation, prime number checking, and greatest common divisor calculation."
        }
    ]
    
    # Write for each language
    languages = ['java', 'python', 'php', 'javascript', 'go', 'ruby']
    
    for lang in languages:
        lang_dir = f'data/code_summarization/code-to-text/{lang}'
        os.makedirs(lang_dir, exist_ok=True)
        
        with open(f'{lang_dir}/test.jsonl', 'w') as f:
            for sample in summarization_samples:
                f.write(json.dumps(sample) + '\n')
    
    print(f"✓ Created {len(summarization_samples)} summarization samples for {len(languages)} languages")

def create_expanded_refinement_data():
    """Create more code refinement test samples"""
    
    buggy_samples = [
        '''public class Calculator {
    public int add(int a, int b) {
        return a - b;  // Bug: should be a + b
    }
}''',
        '''public class StringUtils {
    public static String reverse(String str) {
        if (str == null) return null;
        return str;  // Bug: should reverse the string
    }
}''',
        '''public class ArrayHelper {
    public static int findMax(int[] arr) {
        if (arr == null || arr.length == 0) return -1;
        int max = arr[0];
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] < max) {  // Bug: should be arr[i] > max
                max = arr[i];
            }
        }
        return max;
    }
}''',
        '''public class FileHandler {
    public static void writeToFile(String filename, String content) {
        try (FileWriter writer = new FileWriter(filename)) {
            writer.write(content);
            writer.flush();  // Bug: missing close() or use try-with-resources
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}''',
        '''public class MathUtils {
    public static boolean isPrime(int n) {
        if (n < 2) return false;
        for (int i = 2; i < n; i++) {  // Bug: should be i <= Math.sqrt(n)
            if (n % i == 0) return false;
        }
        return true;
    }
}'''
    ]
    
    fixed_samples = [
        '''public class Calculator {
    public int add(int a, int b) {
        return a + b;  // Fixed: correct addition
    }
}''',
        '''public class StringUtils {
    public static String reverse(String str) {
        if (str == null) return null;
        return new StringBuilder(str).reverse().toString();  // Fixed: proper string reversal
    }
}''',
        '''public class ArrayHelper {
    public static int findMax(int[] arr) {
        if (arr == null || arr.length == 0) return -1;
        int max = arr[0];
        for (int i = 1; i < arr.length; i++) {
            if (arr[i] > max) {  // Fixed: correct comparison
                max = arr[i];
            }
        }
        return max;
    }
}''',
        '''public class FileHandler {
    public static void writeToFile(String filename, String content) {
        try (FileWriter writer = new FileWriter(filename)) {
            writer.write(content);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}''',
        '''public class MathUtils {
    public static boolean isPrime(int n) {
        if (n < 2) return false;
        for (int i = 2; i <= Math.sqrt(n); i++) {  // Fixed: optimized loop
            if (n % i == 0) return false;
        }
        return true;
    }
}'''
    ]
    
    # Write for both small and medium datasets
    for dataset in ['small', 'medium']:
        dataset_dir = f'data/code_refinement/{dataset}'
        os.makedirs(dataset_dir, exist_ok=True)
        
        with open(f'{dataset_dir}/test.buggy-fixed.buggy', 'w') as f:
            for sample in buggy_samples:
                f.write(sample + '\n')
        
        with open(f'{dataset_dir}/test.buggy-fixed.fixed', 'w') as f:
            for sample in fixed_samples:
                f.write(sample + '\n')
    
    print(f"✓ Created {len(buggy_samples)} refinement samples for small and medium datasets")

def main():
    """Main function to expand all test data"""
    print("Expanding test data for CodeAttack...")
    
    # Create directories if they don't exist
    os.makedirs('data/code_translation', exist_ok=True)
    os.makedirs('data/code_summarization/code-to-text', exist_ok=True)
    os.makedirs('data/code_refinement', exist_ok=True)
    
    # Expand each type of data
    create_expanded_translation_data()
    create_expanded_summarization_data()
    create_expanded_refinement_data()
    
    print("\n✓ All test data expanded successfully!")
    print("Now you have:")
    print("- 5 translation samples (Java ↔ C#)")
    print("- 5 summarization samples for each language")
    print("- 5 refinement samples (buggy-fixed pairs)")

if __name__ == "__main__":
    main() 