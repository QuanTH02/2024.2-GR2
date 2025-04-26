from typing import List, Dict, Any
import numpy as np
from nltk.translate.bleu_score import sentence_bleu
from codebleu import calc_codebleu

def calculate_codebleu(original: str, adversarial: str) -> float:
    """
    Calculate CodeBLEU score between original and adversarial code
    
    Args:
        original: Original code snippet
        adversarial: Adversarial code snippet
        
    Returns:
        CodeBLEU score
    """
    # Tokenize code
    original_tokens = tokenize_code(original)
    adversarial_tokens = tokenize_code(adversarial)
    
    # Calculate CodeBLEU
    score = calc_codebleu(
        [original_tokens],
        [adversarial_tokens],
        lang="python",  # Default language
        weights=(0.25, 0.25, 0.25, 0.25)
    )
    
    return score

def calculate_bleu(reference: str, candidate: str) -> float:
    """
    Calculate BLEU score between reference and candidate text
    
    Args:
        reference: Reference text
        candidate: Candidate text
        
    Returns:
        BLEU score
    """
    # Tokenize text
    reference_tokens = reference.split()
    candidate_tokens = candidate.split()
    
    # Calculate BLEU score
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
    """
    Calculate comprehensive attack metrics
    
    Args:
        original_outputs: List of original model outputs
        adversarial_outputs: List of adversarial model outputs
        original_codes: List of original code snippets
        adversarial_codes: List of adversarial code snippets
        
    Returns:
        Dictionary of attack metrics
    """
    metrics = {}
    
    # Calculate performance drop
    original_scores = [calculate_codebleu(ref, cand) for ref, cand in zip(original_outputs, original_codes)]
    adversarial_scores = [calculate_codebleu(ref, cand) for ref, cand in zip(original_outputs, adversarial_outputs)]
    metrics["performance_drop"] = np.mean([orig - adv for orig, adv in zip(original_scores, adversarial_scores)])
    
    # Calculate success rate
    success_count = sum(1 for orig, adv in zip(original_scores, adversarial_scores) if orig - adv > 0)
    metrics["success_rate"] = success_count / len(original_scores)
    
    # Calculate code similarity
    similarities = [calculate_codebleu(orig, adv) for orig, adv in zip(original_codes, adversarial_codes)]
    metrics["code_similarity"] = np.mean(similarities)
    
    # Calculate perturbation rate
    perturbations = [len(set(orig.split()) - set(adv.split())) for orig, adv in zip(original_codes, adversarial_codes)]
    metrics["avg_perturbations"] = np.mean(perturbations)
    
    return metrics

def tokenize_code(code: str) -> List[str]:
    """
    Tokenize code into tokens
    
    Args:
        code: Input code snippet
        
    Returns:
        List of tokens
    """
    # Simple tokenization - split on whitespace and punctuation
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