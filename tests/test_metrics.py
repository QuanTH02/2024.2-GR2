import pytest
from src.utils.metrics import (
    calculate_similarity,
    calculate_attack_metrics,
    calculate_model_metrics,
    calculate_embedding_similarity
)
import torch
from transformers import AutoTokenizer

@pytest.fixture
def tokenizer():
    return AutoTokenizer.from_pretrained("Salesforce/codet5-base")

def test_calculate_similarity():
    # Test identical code
    code1 = "def add(a, b): return a + b"
    code2 = "def add(a, b): return a + b"
    assert calculate_similarity(code1, code2) == 1.0
    
    # Test different code
    code1 = "def add(a, b): return a + b"
    code2 = "def subtract(a, b): return a - b"
    similarity = calculate_similarity(code1, code2)
    assert 0.0 <= similarity <= 1.0
    assert similarity < 1.0
    
    # Test empty code
    assert calculate_similarity("", "") == 1.0
    assert calculate_similarity("def add():", "") < 1.0

def test_calculate_attack_metrics():
    results = [
        {
            'original_code': "def add(a, b): return a + b",
            'adversarial_code': "def add(a, b): return a - b",
            'perturbations': 1,
            'similarity': 0.8
        },
        {
            'original_code': "def multiply(x, y): return x * y",
            'adversarial_code': "def multiply(x, y): return x / y",
            'perturbations': 1,
            'similarity': 0.7
        }
    ]
    
    metrics = calculate_attack_metrics(results)
    assert 'performance_drop' in metrics
    assert 'success_rate' in metrics
    assert 'code_similarity' in metrics
    assert 'avg_perturbations' in metrics
    
    assert 0.0 <= metrics['performance_drop'] <= 1.0
    assert 0.0 <= metrics['success_rate'] <= 1.0
    assert 0.0 <= metrics['code_similarity'] <= 1.0
    assert metrics['avg_perturbations'] > 0

def test_calculate_model_metrics(tokenizer):
    model_outputs = [
        "def add(a, b): return a + b",
        "def multiply(x, y): return x * y"
    ]
    target_outputs = [
        "def add(a, b): return a + b",
        "def multiply(x, y): return x * y"
    ]
    
    metrics = calculate_model_metrics(model_outputs, target_outputs, tokenizer)
    assert 'exact_match' in metrics
    assert 'token_accuracy' in metrics
    assert 'bleu_score' in metrics
    
    assert 0.0 <= metrics['exact_match'] <= 1.0
    assert 0.0 <= metrics['token_accuracy'] <= 1.0
    assert 0.0 <= metrics['bleu_score'] <= 1.0

def test_calculate_embedding_similarity():
    # Create random embeddings
    emb1 = torch.randn(10, 768)
    emb2 = torch.randn(10, 768)
    
    similarity = calculate_embedding_similarity(emb1, emb2)
    assert 0.0 <= similarity <= 1.0
    
    # Test identical embeddings
    similarity = calculate_embedding_similarity(emb1, emb1)
    assert similarity == 1.0 