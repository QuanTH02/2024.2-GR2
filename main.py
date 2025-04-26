import sys
import os

# Thêm thư mục gốc vào path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from examples.example import run_example

def main():
    # Chạy ví dụ
    result = run_example()
    
    # In kết quả
    print("Code gốc:")
    print(result["original_code"])
    print("\nCode đã bị tấn công:")
    print(result["adversarial_code"])
    print("\nSố token đã thay đổi:", result["perturbations"])
    print("Độ tương đồng:", result["similarity"])

if __name__ == "__main__":
    main() 