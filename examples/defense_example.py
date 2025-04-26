from codeattack import Attack, AttackArgs
from codeattack.models import CodeBERT
from codeattack.attacks import TokenSubstitutionAttack
from codeattack.defenses import AdversarialTraining

def main():
    # Khởi tạo mô hình CodeBERT
    model = CodeBERT()
    
    # Tạo dữ liệu huấn luyện
    training_codes = [
        """
def calculate_sum(a, b):
    return a + b
""",
        """
def find_max(numbers):
    return max(numbers)
"""
    ]
    
    # Khởi tạo phương pháp phòng thủ
    defense = AdversarialTraining()
    
    # Huấn luyện mô hình với phòng thủ
    defended_model = defense.train(
        model=model,
        training_codes=training_codes,
        epochs=5,
        batch_size=2
    )
    
    # Tạo một đoạn mã nguồn mẫu để kiểm tra
    test_code = """
def calculate_average(numbers):
    return sum(numbers) / len(numbers)
"""
    
    # Khởi tạo tấn công
    attack = TokenSubstitutionAttack()
    
    # Cấu hình tham số tấn công
    attack_args = AttackArgs(
        num_examples=1,
        disable_stdout=True
    )
    
    # Thực hiện tấn công trên mô hình đã được phòng thủ
    results = attack.attack(test_code, defended_model, attack_args)
    
    # In kết quả
    print("Mã nguồn gốc:")
    print(test_code)
    print("\nMã nguồn sau khi tấn công:")
    print(results.perturbed_text)
    print("\nKết quả dự đoán của mô hình:")
    print(f"Độ chính xác: {results.accuracy:.2%}")

if __name__ == "__main__":
    main() 