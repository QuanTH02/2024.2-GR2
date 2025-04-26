from typing import List, Dict, Any
import numpy as np
from nltk.translate.bleu_score import sentence_bleu
from codebleu import calc_codebleu

def calculate_codebleu(original: str, adversarial: str) -> float:
    original_tokens = tokenize_code(original)
    adversarial_tokens = tokenize_code(adversarial)
    
    score = calc_codebleu(
        [original_tokens],
        [adversarial_tokens],
        lang="python",
        weights=(0.25, 0.25, 0.25, 0.25)
    )
    
    return score

def calculate_bleu(reference: str, candidate: str) -> float:
    reference_tokens = reference.split()
    candidate_tokens = candidate.split()
    
    score = sentence_bleu(
        [reference_tokens],
        candidate_tokens,
        weights=(0.25, 0.25, 0.25, 0.25)
    )
    
    return score

def calculate_attack_metrics(
    original_outputs: List[str],
    adversarial_outputs: List[str],
    original_codes: List[str],
    adversarial_codes: List[str]
) -> Dict[str, float]:
    metrics = {}
    
    original_scores = [calculate_codebleu(ref, cand) for ref, cand in zip(original_outputs, original_codes)]
    adversarial_scores = [calculate_codebleu(ref, cand) for ref, cand in zip(original_outputs, adversarial_outputs)]
    metrics["performance_drop"] = np.mean([orig - adv for orig, adv in zip(original_scores, adversarial_scores)])
    
    success_count = sum(1 for orig, adv in zip(original_scores, adversarial_scores) if orig - adv > 0)
    metrics["success_rate"] = success_count / len(original_scores)
    
    similarities = [calculate_codebleu(orig, adv) for orig, adv in zip(original_codes, adversarial_codes)]
    metrics["code_similarity"] = np.mean(similarities)
    
    perturbations = [len(set(orig.split()) - set(adv.split())) for orig, adv in zip(original_codes, adversarial_codes)]
    metrics["avg_perturbations"] = np.mean(perturbations)
    
    return metrics

def tokenize_code(code: str) -> List[str]:
    tokens = []
    current_token = ""
    
    for char in code:
        if char.isspace() or char in "(){}[].,;+-*/%=<>!&|^~":
            if current_token:
                tokens.append(current_token)
                current_token = ""
            if not char.isspace():
                tokens.append(char)
        else:
            current_token += char
            
    if current_token:
        tokens.append(current_token)
        
    return tokens 