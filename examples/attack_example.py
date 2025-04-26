import sys
import os

# Thêm thư mục gốc của dự án vào PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.attack.attack import CodeAttack
from src.utils.file_utils import load_code_from_file, save_code_to_file

def main():
    # Khởi tạo đối tượng tấn công
    attack = CodeAttack()
    
    # Tạo một đoạn mã nguồn mẫu
    original_code = """
def calculate_sum(a, b):
    return a + b
"""
    
    # Thực hiện tấn công
    perturbed_code = attack.attack(original_code)
    
    # In kết quả
    print("Mã nguồn gốc:")
    print(original_code)
    print("\nMã nguồn sau khi tấn công:")
    print(perturbed_code)

if __name__ == "__main__":
    main() 