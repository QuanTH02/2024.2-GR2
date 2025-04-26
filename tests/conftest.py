import pytest
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from src.attacks.attack import CodeAttack

@pytest.fixture(scope="session")
def model_and_tokenizer():
    model_name = "Salesforce/codet5-base"
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer

@pytest.fixture(scope="session")
def attack(model_and_tokenizer):
    model, tokenizer = model_and_tokenizer
    return CodeAttack(model=model, tokenizer=tokenizer)

@pytest.fixture(scope="session")
def device():
    return torch.device('cuda' if torch.cuda.is_available() else 'cpu') 