import numpy as np
from typing import List, Dict, Any
from Levenshtein import distance
from sklearn.metrics.pairwise import cosine_similarity
import torch
from transformers import PreTrainedTokenizer

def calculate_similarity(code1: str, code2: str) -> float:
    tokens1 = code1.split()
    tokens2 = code2.split()
    
    lev_distance = distance(tokens1, tokens2)
    
    max_len = max(len(tokens1), len(tokens2))
    if max_len == 0:
        return 1.0
    
    similarity = 1 - (lev_distance / max_len)
    return similarity

def calculate_attack_metrics(results: List[Dict[str, Any]]) -> Dict[str, float]:
    performance_drop = np.mean([1 - r['similarity'] for r in results])
    success_rate = np.mean([r['similarity'] < 0.5 for r in results])
    code_similarity = np.mean([r['similarity'] for r in results])
    avg_perturbations = np.mean([r['perturbations'] for r in results])
    
    return {
        'performance_drop': performance_drop,
        'success_rate': success_rate,
        'code_similarity': code_similarity,
        'avg_perturbations': avg_perturbations
    }

def calculate_model_metrics(
    model_outputs: List[str],
    target_outputs: List[str],
    tokenizer: PreTrainedTokenizer
) -> Dict[str, float]:
    model_tokens = [tokenizer.tokenize(output) for output in model_outputs]
    target_tokens = [tokenizer.tokenize(output) for output in target_outputs]
    
    exact_match = np.mean([
        m == t for m, t in zip(model_tokens, target_tokens)
    ])
    
    token_accuracy = np.mean([
        sum(1 for a, b in zip(m, t) if a == b) / max(len(m), len(t))
        for m, t in zip(model_tokens, target_tokens)
    ])
    
    from nltk.translate.bleu_score import sentence_bleu
    bleu_score = np.mean([
        sentence_bleu([t], m)
        for m, t in zip(model_tokens, target_tokens)
    ])
    
    return {
        'exact_match': exact_match,
        'token_accuracy': token_accuracy,
        'bleu_score': bleu_score
    }

def calculate_embedding_similarity(
    embeddings1: torch.Tensor,
    embeddings2: torch.Tensor
) -> float:
    emb1 = embeddings1.cpu().numpy()
    emb2 = embeddings2.cpu().numpy()
    
    emb1 = emb1 / (np.linalg.norm(emb1, axis=1, keepdims=True) + 1e-8)
    emb2 = emb2 / (np.linalg.norm(emb2, axis=1, keepdims=True) + 1e-8)
    
    similarity = cosine_similarity(emb1, emb2)
    
    if np.array_equal(emb1, emb2):
        return 1.0
        
    similarity = np.clip(similarity, 0, 1)
        
    return float(similarity.mean()) 