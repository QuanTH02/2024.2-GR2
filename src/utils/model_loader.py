from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

def load_model(model_name: str):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    
    return model, tokenizer

def save_model(model, tokenizer, model_name: str):
    model.save_pretrained(f'data/models/{model_name}')
    
    tokenizer.save_pretrained(f'data/models/{model_name}') 