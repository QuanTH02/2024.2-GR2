from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from src.attack.attack import CodeAttack
from src.evaluation.metrics import calculate_attack_metrics

def main():
    # Load a pre-trained model (e.g., CodeT5)
    model_name = "Salesforce/codet5-base"
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    # Initialize CodeAttack
    attack = CodeAttack(
        model=model,
        max_perturbations=0.4,
        similarity_threshold=0.5
    )
    
    # Example code snippets
    original_codes = [
        """
        public class Calculator {
            public int add(int a, int b) {
                return a + b;
            }
        }
        """,
        """
        def calculate_average(numbers):
            total = sum(numbers)
            return total / len(numbers)
        """
    ]
    
    # Generate adversarial examples
    adversarial_codes = []
    for code in original_codes:
        result = attack.generate(code)
        adversarial_codes.append(result["adversarial_code"])
        print(f"\nOriginal code:\n{code}")
        print(f"\nAdversarial code:\n{result['adversarial_code']}")
        print(f"\nNumber of perturbations: {result['perturbations']}")
        print(f"Similarity score: {result['similarity']:.2f}")
    
    # Get model outputs
    original_outputs = []
    adversarial_outputs = []
    
    for orig_code, adv_code in zip(original_codes, adversarial_codes):
        # Tokenize inputs
        orig_inputs = tokenizer(orig_code, return_tensors="pt")
        adv_inputs = tokenizer(adv_code, return_tensors="pt")
        
        # Get model outputs
        with torch.no_grad():
            orig_output = model.generate(**orig_inputs)
            adv_output = model.generate(**adv_inputs)
            
        # Decode outputs
        orig_output_text = tokenizer.decode(orig_output[0], skip_special_tokens=True)
        adv_output_text = tokenizer.decode(adv_output[0], skip_special_tokens=True)
        
        original_outputs.append(orig_output_text)
        adversarial_outputs.append(adv_output_text)
    
    # Calculate attack metrics
    metrics = calculate_attack_metrics(
        original_outputs=original_outputs,
        adversarial_outputs=adversarial_outputs,
        original_codes=original_codes,
        adversarial_codes=adversarial_codes
    )
    
    print("\nAttack Metrics:")
    print(f"Performance drop: {metrics['performance_drop']:.2f}")
    print(f"Success rate: {metrics['success_rate']:.2f}")
    print(f"Code similarity: {metrics['code_similarity']:.2f}")
    print(f"Average perturbations: {metrics['avg_perturbations']:.2f}")

if __name__ == "__main__":
    main() 