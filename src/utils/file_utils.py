import json
import os

def save_results(results, output_file):
    """
    Lưu kết quả tấn công vào file
    
    Args:
        results: Dictionary chứa kết quả
        output_file: Đường dẫn file output
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

def load_code_from_file(file_path):
    """
    Đọc code từ file
    
    Args:
        file_path: Đường dẫn file chứa code
        
    Returns:
        Nội dung code
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def save_code_to_file(code, output_file):
    """
    Lưu code vào file
    
    Args:
        code: Nội dung code
        output_file: Đường dẫn file output
    """
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(code) 