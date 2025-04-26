import sys
import os
import argparse
from pathlib import Path

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from src.attacks.attack import CodeAttack
from src.evaluation.metrics import calculate_attack_metrics
from src.utils.data_loader import load_dataset
from src.utils.model_loader import load_model

def parse_args():
    parser = argparse.ArgumentParser(description='CodeAttack: Code-Based Adversarial Attacks')
    parser.add_argument('--model_name', type=str, default='Salesforce/codet5-base',
                      help='Name of the pre-trained model to use')
    parser.add_argument('--dataset_name', type=str, required=True,
                      help='Name of the dataset to use')
    parser.add_argument('--max_perturbations', type=float, default=0.4,
                      help='Maximum number of perturbations allowed')
    parser.add_argument('--similarity_threshold', type=float, default=0.5,
                      help='Minimum similarity threshold for adversarial examples')
    parser.add_argument('--output_dir', type=str, default='results',
                      help='Directory to save results')
    return parser.parse_args()

def main():
    args = parse_args()
    
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    model, tokenizer = load_model(args.model_name)
    
    dataset = load_dataset(args.dataset_name)
    
    attack = CodeAttack(
        model=model,
        tokenizer=tokenizer,
        max_perturbations=args.max_perturbations,
        similarity_threshold=args.similarity_threshold
    )
    
    results = []
    for code in dataset:
        result = attack.generate(code)
        results.append(result)
        
        print(f"\nCode gốc:\n{result['original_code']}")
        print(f"\nCode đã bị tấn công:\n{result['adversarial_code']}")
        print(f"\nSố token đã thay đổi: {result['perturbations']}")
        print(f"Độ tương đồng: {result['similarity']:.2f}")
    
    metrics = calculate_attack_metrics(results)
    
    print("\nAttack Metrics:")
    print(f"Performance drop: {metrics['performance_drop']:.2f}")
    print(f"Success rate: {metrics['success_rate']:.2f}")
    print(f"Code similarity: {metrics['code_similarity']:.2f}")
    print(f"Average perturbations: {metrics['avg_perturbations']:.2f}")
    
    import json
    with open(output_dir / 'results.json', 'w') as f:
        json.dump({
            'args': vars(args),
            'metrics': metrics,
            'results': results
        }, f, indent=2)

if __name__ == "__main__":
    main() 