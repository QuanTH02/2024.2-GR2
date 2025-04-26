import torch
import numpy as np
from typing import List, Dict, Any
from transformers import AutoModelForMaskedLM, AutoTokenizer

from ..constraints.code_constraints import CodeConstraints
from ..evaluation.metrics import calculate_codebleu, calculate_bleu
from ..utils.tokenizer import CodeTokenizer

class CodeAttack:
    def __init__(
        self,
        model: Any,
        max_perturbations: float = 3,
        similarity_threshold: float = 0.8,
        top_k: int = 50
    ):
        self.model = model
        self.max_perturbations = max_perturbations
        self.similarity_threshold = similarity_threshold
        self.top_k = top_k
        
        self.codebert = AutoModelForMaskedLM.from_pretrained("microsoft/codebert-base-mlm")
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base-mlm")
        
        self.constraints = CodeConstraints()
        
        self.code_tokenizer = CodeTokenizer()
        
    def find_vulnerable_tokens(self, code: str) -> List[Dict[str, Any]]:
        tokens = code.split()
        vulnerable_tokens = []
        
        for i, token in enumerate(tokens):
            masked_tokens = tokens.copy()
            masked_tokens[i] = "[MASK]"
            masked_code = " ".join(masked_tokens)
            
            original_output = self.model(code)
            masked_output = self.model(masked_code)
            
            influence_score = self._calculate_influence_score(original_output, masked_output)
            
            vulnerable_tokens.append((i, token, influence_score))
        
        vulnerable_tokens.sort(key=lambda x: x[2], reverse=True)
        return vulnerable_tokens[:self.max_perturbations]
    
    def _calculate_influence_score(self, original_output: torch.Tensor, masked_output: torch.Tensor) -> float:
        return np.abs(original_output - masked_output).sum()
    
    def generate_substitutes(self, token: str) -> List[str]:
        substitutes = [
            token.upper(),
            token.lower(),
            token + "1",
            "var_" + token,
            token + "_var",
            token + "x",
            "new_" + token,
            token + "_new"
        ]
        return substitutes
    
    def generate(self, code: str, target_output: str = None) -> Dict[str, Any]:
        vulnerable_tokens = self.find_vulnerable_tokens(code)
        
        tokens = code.split()
        variable_map = {}
        
        for i, original_token, _ in vulnerable_tokens:
            if original_token in ["def", "return"]:
                continue
                
            substitutes = self.generate_substitutes(original_token)
            
            for substitute in substitutes:
                if (original_token.isidentifier() and not original_token[0].isdigit()) or original_token in ["+", "-", "*", "/"]:
                    variable_map[original_token] = substitute
                    break
        
        for i, token in enumerate(tokens):
            if token in variable_map:
                tokens[i] = variable_map[token]
        
        adversarial_code = " ".join(tokens)
        
        return {
            "original_code": code,
            "adversarial_code": adversarial_code,
            "perturbations": len(variable_map),
            "similarity": self._calculate_similarity(code, adversarial_code)
        }
    
    def _check_similarity(self, original: str, adversarial: str) -> bool:
        similarity = self._calculate_similarity(original, adversarial)
        return similarity >= self.similarity_threshold
    
    def _calculate_similarity(self, original: str, adversarial: str) -> float:
        original_tokens = set(original.split())
        adversarial_tokens = set(adversarial.split())
        intersection = original_tokens.intersection(adversarial_tokens)
        union = original_tokens.union(adversarial_tokens)
        return len(intersection) / len(union) if union else 0.0
    
    def _is_attack_successful(self, code: str, target_output: str = None) -> bool:
        output = self.model(code)
        
        if target_output is not None:
            return calculate_bleu(output, target_output) < self.similarity_threshold
        else:
            original_output = self.model(self.original_code)
            return calculate_bleu(output, original_output) < self.similarity_threshold
    
    def _is_valid_substitution(self, code: str) -> bool:
        try:
            compile(code, "<string>", "exec")
            return True
        except:
            return False 