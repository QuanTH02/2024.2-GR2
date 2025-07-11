#!/usr/bin/env python3
"""
Script to create a large test dataset for CodeAttack evaluation
This will generate 50+ samples for each task type
"""

import os
import json
import random

def generate_java_classes():
    """Generate diverse Java class samples"""
    classes = []
    
    # Basic utility classes
    basic_classes = [
        ("Calculator", "Basic arithmetic operations"),
        ("StringUtils", "String manipulation utilities"),
        ("ArrayHelper", "Array processing utilities"),
        ("FileHandler", "File I/O operations"),
        ("MathUtils", "Mathematical functions"),
        ("DateUtils", "Date and time utilities"),
        ("NetworkUtils", "Network operations"),
        ("DatabaseHelper", "Database operations"),
        ("EncryptionUtils", "Encryption and security"),
        ("ValidationUtils", "Input validation utilities")
    ]
    
    for class_name, description in basic_classes:
        # Generate different complexity levels
        for complexity in ["simple", "medium", "complex"]:
            if complexity == "simple":
                code = f'''public class {class_name} {{
    public static String getInfo() {{
        return "{description}";
    }}
}}'''
            elif complexity == "medium":
                code = f'''public class {class_name} {{
    private static final String INFO = "{description}";
    
    public static String getInfo() {{
        return INFO;
    }}
    
    public static boolean isValid(String input) {{
        return input != null && !input.trim().isEmpty();
    }}
    
    public static String process(String data) {{
        if (!isValid(data)) return null;
        return data.trim().toLowerCase();
    }}
}}'''
            else:  # complex
                code = f'''public class {class_name} {{
    private static final String INFO = "{description}";
    private static final int MAX_RETRIES = 3;
    private static final double TIMEOUT = 30.0;
    
    public static String getInfo() {{
        return INFO;
    }}
    
    public static boolean isValid(String input) {{
        return input != null && !input.trim().isEmpty();
    }}
    
    public static String process(String data) {{
        if (!isValid(data)) return null;
        return data.trim().toLowerCase();
    }}
    
    public static Result executeWithRetry(String input) {{
        int attempts = 0;
        while (attempts < MAX_RETRIES) {{
            try {{
                String result = process(input);
                if (result != null) {{
                    return new Result(true, result, null);
                }}
            }} catch (Exception e) {{
                attempts++;
                if (attempts >= MAX_RETRIES) {{
                    return new Result(false, null, e.getMessage());
                }}
            }}
        }}
        return new Result(false, null, "Max retries exceeded");
    }}
    
    public static class Result {{
        private final boolean success;
        private final String data;
        private final String error;
        
        public Result(boolean success, String data, String error) {{
            this.success = success;
            this.data = data;
            this.error = error;
        }}
        
        public boolean isSuccess() {{ return success; }}
        public String getData() {{ return data; }}
        public String getError() {{ return error; }}
    }}
}}'''
            
            classes.append((code, f"{class_name} class with {complexity} implementation"))
    
    return classes

def generate_cs_classes():
    """Generate corresponding C# class samples"""
    classes = []
    
    basic_classes = [
        ("Calculator", "Basic arithmetic operations"),
        ("StringUtils", "String manipulation utilities"),
        ("ArrayHelper", "Array processing utilities"),
        ("FileHandler", "File I/O operations"),
        ("MathUtils", "Mathematical functions"),
        ("DateUtils", "Date and time utilities"),
        ("NetworkUtils", "Network operations"),
        ("DatabaseHelper", "Database operations"),
        ("EncryptionUtils", "Encryption and security"),
        ("ValidationUtils", "Input validation utilities")
    ]
    
    for class_name, description in basic_classes:
        for complexity in ["simple", "medium", "complex"]:
            if complexity == "simple":
                code = f'''using System;

public class {class_name} {{
    public static string GetInfo() {{
        return "{description}";
    }}
}}'''
            elif complexity == "medium":
                code = f'''using System;

public class {class_name} {{
    private static readonly string Info = "{description}";
    
    public static string GetInfo() {{
        return Info;
    }}
    
    public static bool IsValid(string input) {{
        return !string.IsNullOrEmpty(input?.Trim());
    }}
    
    public static string Process(string data) {{
        if (!IsValid(data)) return null;
        return data.Trim().ToLower();
    }}
}}'''
            else:  # complex
                code = f'''using System;

public class {class_name} {{
    private static readonly string Info = "{description}";
    private const int MaxRetries = 3;
    private const double Timeout = 30.0;
    
    public static string GetInfo() {{
        return Info;
    }}
    
    public static bool IsValid(string input) {{
        return !string.IsNullOrEmpty(input?.Trim());
    }}
    
    public static string Process(string data) {{
        if (!IsValid(data)) return null;
        return data.Trim().ToLower();
    }}
    
    public static Result ExecuteWithRetry(string input) {{
        int attempts = 0;
        while (attempts < MaxRetries) {{
            try {{
                string result = Process(input);
                if (result != null) {{
                    return new Result(true, result, null);
                }}
            }} catch (Exception e) {{
                attempts++;
                if (attempts >= MaxRetries) {{
                    return new Result(false, null, e.Message);
                }}
            }}
        }}
        return new Result(false, null, "Max retries exceeded");
    }}
    
    public class Result {{
        public bool Success {{ get; }}
        public string Data {{ get; }}
        public string Error {{ get; }}
        
        public Result(bool success, string data, string error) {{
            Success = success;
            Data = data;
            Error = error;
        }}
    }}
}}'''
            
            classes.append((code, f"{class_name} class with {complexity} implementation"))
    
    return classes

def create_large_translation_dataset():
    """Create a large translation dataset"""
    java_classes = generate_java_classes()
    cs_classes = generate_cs_classes()
    
    # Write Java samples
    with open('data/code_translation/large.java-cs.txt.java', 'w') as f:
        for code, _ in java_classes:
            f.write(code + '\n')
    
    # Write C# samples
    with open('data/code_translation/large.java-cs.txt.cs', 'w') as f:
        for code, _ in cs_classes:
            f.write(code + '\n')
    
    print(f"✓ Created large translation dataset with {len(java_classes)} samples")

def create_large_summarization_dataset():
    """Create a large summarization dataset"""
    java_classes = generate_java_classes()
    
    # Create summarization samples for each language
    languages = ['java', 'python', 'php', 'javascript', 'go', 'ruby']
    
    for lang in languages:
        lang_dir = f'data/code_summarization/code-to-text/{lang}'
        os.makedirs(lang_dir, exist_ok=True)
        
        with open(f'{lang_dir}/large.jsonl', 'w') as f:
            for code, docstring in java_classes:
                sample = {
                    "code": code,
                    "docstring": docstring
                }
                f.write(json.dumps(sample) + '\n')
    
    print(f"✓ Created large summarization dataset with {len(java_classes)} samples for {len(languages)} languages")

def create_large_refinement_dataset():
    """Create a large refinement dataset with buggy-fixed pairs"""
    
    # Generate buggy-fixed pairs
    buggy_fixed_pairs = []
    
    # Simple bugs
    simple_bugs = [
        ('''public class Calculator {
    public int add(int a, int b) {
        return a - b;  // Bug: should be a + b
    }
}''',
     '''public class Calculator {
    public int add(int a, int b) {
        return a + b;  // Fixed: correct addition
    }
}'''),
        ('''public class StringUtils {
    public static String reverse(String str) {
        if (str == null) return null;
        return str;  // Bug: should reverse the string
    }
}''',
     '''public class StringUtils {
    public static String reverse(String str) {
        if (str == null) return null;
        return new StringBuilder(str).reverse().toString();  // Fixed: proper reversal
    }
}'''),
        ('''public class ArrayHelper {
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
}''')
    ]
    
    buggy_fixed_pairs.extend(simple_bugs)
    
    # Medium complexity bugs
    medium_bugs = [
        ('''public class FileHandler {
    public static void writeToFile(String filename, String content) {
        try (FileWriter writer = new FileWriter(filename)) {
            writer.write(content);
            writer.flush();  // Bug: missing close() or use try-with-resources properly
        } catch (IOException e) {
            e.printStackTrace();
        }
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
}'''),
        ('''public class MathUtils {
    public static boolean isPrime(int n) {
        if (n < 2) return false;
        for (int i = 2; i < n; i++) {  // Bug: should be i <= Math.sqrt(n)
            if (n % i == 0) return false;
        }
        return true;
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
}''')
    ]
    
    buggy_fixed_pairs.extend(medium_bugs)
    
    # Complex bugs
    complex_bugs = [
        ('''public class ValidationUtils {
    public static boolean isValidEmail(String email) {
        if (email == null) return false;
        return email.contains("@");  // Bug: too simple validation
    }
    
    public static boolean isValidPhone(String phone) {
        if (phone == null) return false;
        return phone.length() >= 10;  // Bug: too simple validation
    }
}''',
     '''public class ValidationUtils {
    public static boolean isValidEmail(String email) {
        if (email == null) return false;
        String emailRegex = "^[A-Za-z0-9+_.-]+@(.+)$";
        return email.matches(emailRegex);  // Fixed: proper email validation
    }
    
    public static boolean isValidPhone(String phone) {
        if (phone == null) return false;
        String phoneRegex = "^\\d{10,}$";
        return phone.replaceAll("[^\\d]", "").matches(phoneRegex);  // Fixed: proper phone validation
    }
}''')
    ]
    
    buggy_fixed_pairs.extend(complex_bugs)
    
    # Generate more variations
    for i in range(20):  # Add 20 more variations
        buggy_code = f'''public class TestClass{i} {{
    public static int calculate(int x, int y) {{
        return x - y;  // Bug: should be x + y
    }}
    
    public static String process(String input) {{
        if (input == null) return null;
        return input;  // Bug: should process the input
    }}
}}'''
        
        fixed_code = f'''public class TestClass{i} {{
    public static int calculate(int x, int y) {{
        return x + y;  // Fixed: correct calculation
    }}
    
    public static String process(String input) {{
        if (input == null) return null;
        return input.trim().toLowerCase();  // Fixed: proper processing
    }}
}}'''
        
        buggy_fixed_pairs.append((buggy_code, fixed_code))
    
    # Write for both small and medium datasets
    for dataset in ['small', 'medium']:
        dataset_dir = f'data/code_refinement/{dataset}'
        os.makedirs(dataset_dir, exist_ok=True)
        
        with open(f'{dataset_dir}/large.buggy-fixed.buggy', 'w') as f:
            for buggy, _ in buggy_fixed_pairs:
                f.write(buggy + '\n')
        
        with open(f'{dataset_dir}/large.buggy-fixed.fixed', 'w') as f:
            for _, fixed in buggy_fixed_pairs:
                f.write(fixed + '\n')
    
    print(f"✓ Created large refinement dataset with {len(buggy_fixed_pairs)} buggy-fixed pairs")

def update_config_for_large_datasets():
    """Update config to include large dataset options"""
    
    # Read existing config
    with open('configs/config_data.yaml', 'r') as f:
        config = f.read()
    
    # Add large dataset configurations
    large_config_additions = '''
  java_cs_large:
    data_path_x : './data/code_translation/large.java-cs.txt.java'
    data_path_y: './data/code_translation/large.java-cs.txt.cs'

  cs_java_large:
    data_path_x: './data/code_translation/large.java-cs.txt.cs'
    data_path_y : './data/code_translation/large.java-cs.txt.java'

refinement:
  java_small_large:
    data_path_x : './data/code_refinement/small/large.buggy-fixed.buggy'
    data_path_y: './data/code_refinement/small/large.buggy-fixed.fixed'
    
  java_medium_large:
    data_path_x : './data/code_refinement/medium/large.buggy-fixed.buggy'
    data_path_y: './data/code_refinement/medium/large.buggy-fixed.fixed'

summarize:
  ruby_large:
    data_path_x : ./data/code_summarization/code-to-text/ruby/large.jsonl
    data_path_y : ./data/code_summarization/code-to-text/ruby/large.jsonl
  javascript_large:
    data_path_x : ./data/code_summarization/code-to-text/javascript/large.jsonl
    data_path_y : ./data/code_summarization/code-to-text/javascript/large.jsonl
  go_large:
    data_path_x : ./data/code_summarization/code-to-text/go/large.jsonl
    data_path_y : ./data/code_summarization/code-to-text/go/large.jsonl
  python_large:
    data_path_x : ./data/code_summarization/code-to-text/python/large.jsonl
    data_path_y : ./data/code_summarization/code-to-text/python/large.jsonl
  java_large:
    data_path_x : ./data/code_summarization/code-to-text/java/large.jsonl
    data_path_y : ./data/code_summarization/code-to-text/java/large.jsonl
  php_large:
    data_path_x : ./data/code_summarization/code-to-text/php/large.jsonl
    data_path_y : ./data/code_summarization/code-to-text/php/large.jsonl
'''
    
    # Insert after existing translation section
    config = config.replace('cs_java:\n    data_path_x:', 'cs_java:\n    data_path_x:' + large_config_additions)
    
    # Write updated config
    with open('configs/config_data.yaml', 'w') as f:
        f.write(config)
    
    print("✓ Updated config_data.yaml with large dataset options")

def main():
    """Main function to create large test datasets"""
    print("Creating large test datasets for CodeAttack...")
    
    # Create directories
    os.makedirs('data/code_translation', exist_ok=True)
    os.makedirs('data/code_summarization/code-to-text', exist_ok=True)
    os.makedirs('data/code_refinement', exist_ok=True)
    
    # Create large datasets
    create_large_translation_dataset()
    create_large_summarization_dataset()
    create_large_refinement_dataset()
    update_config_for_large_datasets()
    
    print("\n✓ All large test datasets created successfully!")
    print("Now you have:")
    print("- 30+ translation samples (Java ↔ C#)")
    print("- 30+ summarization samples for each language")
    print("- 25+ refinement samples (buggy-fixed pairs)")
    print("- Updated config with 'large' dataset options")
    print("\nTo use large datasets, add '_large' to your language parameter:")
    print("Example: --lang java_cs_large")

if __name__ == "__main__":
    main() 