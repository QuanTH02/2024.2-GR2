from src.attack.attack import CodeAttack
from src.utils.file_utils import load_code_from_file, save_code_to_file
from src.config import *
from src.models.target_model import TargetModel

def main():
    # Example target code
    target_code = """
def calculate_sum(a, b):
    return a + b
    """
    
    # Initialize the model
    model = TargetModel(MODEL_NAME)
    
    # Initialize the attack
    attack = CodeAttack(
        model=model,
        max_perturbations=MAX_PERTURBATIONS,
        similarity_threshold=SIMILARITY_THRESHOLD
    )
    
    # Generate adversarial example
    result = attack.generate(target_code)
    
    # Save results
    print("Original code:")
    print(result["original_code"])
    print("\nAdversarial code:")
    print(result["adversarial_code"])
    print("\nNumber of perturbations:", result["perturbations"])
    print("Similarity score:", result["similarity"])
    
    # Save to files
    if SAVE_RESULTS:
        save_code_to_file(result["original_code"], f"{OUTPUT_DIR}/original.py")
        save_code_to_file(result["adversarial_code"], f"{OUTPUT_DIR}/adversarial.py")

if __name__ == "__main__":
    main() 