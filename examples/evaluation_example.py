from codeattack import Attack, AttackArgs
from codeattack.models import CodeBERT
from codeattack.attacks import TokenSubstitutionAttack
from codeattack.evaluation import evaluate_model

def main():
    # Khởi tạo mô hình CodeBERT
    model = CodeBERT()
    
    # Tạo danh sách các đoạn mã nguồn mẫu
    test_codes = [
        """
def calculate_sum(a, b):
    return a + b
""",
        """
def find_max(numbers):
    return max(numbers)
"""
    ]
    
    # Khởi tạo tấn công
    attack = TokenSubstitutionAttack()
    
    # Cấu hình tham số đánh giá
    attack_args = AttackArgs(
        num_examples=len(test_codes),
        disable_stdout=True
    )
    
    # Đánh giá mô hình
    results = evaluate_model(
        model=model,
        attack=attack,
        attack_args=attack_args,
        test_codes=test_codes
    )
    
    # In kết quả đánh giá
    print("Kết quả đánh giá:")
    print(f"Tỷ lệ tấn công thành công: {results.success_rate:.2%}")
    print(f"Thời gian trung bình mỗi tấn công: {results.avg_time:.2f} giây")

if __name__ == "__main__":
    main() 