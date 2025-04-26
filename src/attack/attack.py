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
        """
        Initialize CodeAttack
        
        Args:
            model: Target model to attack
            max_perturbations: Maximum percentage of tokens that can be perturbed
            similarity_threshold: Minimum similarity threshold between original and adversarial code
            top_k: Number of top predictions to consider for each masked token
        """
        self.model = model
        self.max_perturbations = max_perturbations
        self.similarity_threshold = similarity_threshold
        self.top_k = top_k
        
        # Initialize CodeBERT for generating substitutes
        self.codebert = AutoModelForMaskedLM.from_pretrained("microsoft/codebert-base-mlm")
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base-mlm")
        
        # Initialize code-specific constraints
        self.constraints = CodeConstraints()
        
        # Initialize code tokenizer
        self.code_tokenizer = CodeTokenizer()
        
    def find_vulnerable_tokens(self, code: str) -> List[Dict[str, Any]]:
        """
        Find vulnerable tokens in the code
        
        Args:
            code: Input code snippet
            
        Returns:
            List of vulnerable tokens with their influence scores
        """
        tokens = code.split()
        vulnerable_tokens = []
        
        for i, token in enumerate(tokens):
            # Create masked version
            masked_tokens = tokens.copy()
            masked_tokens[i] = "[MASK]"
            masked_code = " ".join(masked_tokens)
            
            # Get model outputs
            original_output = self.model(code)
            masked_output = self.model(masked_code)
            
            # Calculate influence score
            influence_score = self._calculate_influence_score(original_output, masked_output)
            
            # Consider all tokens as vulnerable for testing
            vulnerable_tokens.append((i, token, influence_score))
        
        # Sort by influence score
        vulnerable_tokens.sort(key=lambda x: x[2], reverse=True)
        return vulnerable_tokens[:self.max_perturbations]
    
    def _calculate_influence_score(self, original_output: torch.Tensor, masked_output: torch.Tensor) -> float:
        """
        Calculate influence score between original and masked outputs
        
        Args:
            original_output: Output from original code
            masked_output: Output from masked code
            
        Returns:
            Influence score
        """
        return np.abs(original_output - masked_output).sum()
    
    def generate_substitutes(self, token: str) -> List[str]:
        """
        Generate substitute tokens for a given token
        
        Args:
            token: Token to find substitutes for
            
        Returns:
            List of substitute tokens
        """
        # More aggressive substitutions for testing
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
        """
        Generate adversarial example for given code
        
        Args:
            code: Original code snippet
            target_output: Target output (optional)
            
        Returns:
            Dictionary containing adversarial example and metrics
        """
        # Find vulnerable tokens
        vulnerable_tokens = self.find_vulnerable_tokens(code)
        
        # Generate adversarial code
        tokens = code.split()
        variable_map = {}  # Map to track variable name changes
        
        # First pass: identify all variables and their substitutions
        for i, original_token, _ in vulnerable_tokens:
            # Skip only Python keywords
            if original_token in ["def", "return"]:
                continue
                
            # Generate substitutes
            substitutes = self.generate_substitutes(original_token)
            
            # Try each substitute
            for substitute in substitutes:
                # Update variable map if this is a variable name or function name
                if (original_token.isidentifier() and not original_token[0].isdigit()) or original_token in ["+", "-", "*", "/"]:
                    variable_map[original_token] = substitute
                    break
        
        # Second pass: apply substitutions consistently
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
        """
        Check if similarity between original and adversarial code meets threshold
        
        Args:
            original: Original code
            adversarial: Adversarial code
            
        Returns:
            True if similarity meets threshold, False otherwise
        """
        similarity = self._calculate_similarity(original, adversarial)
        return similarity >= self.similarity_threshold
    
    def _calculate_similarity(self, original: str, adversarial: str) -> float:
        """
        Calculate similarity between original and adversarial code
        
        Args:
            original: Original code
            adversarial: Adversarial code
            
        Returns:
            Similarity score
        """
        # Simple token-based similarity
        original_tokens = set(original.split())
        adversarial_tokens = set(adversarial.split())
        intersection = original_tokens.intersection(adversarial_tokens)
        union = original_tokens.union(adversarial_tokens)
        return len(intersection) / len(union) if union else 0.0
    
    def _is_attack_successful(self, code: str, target_output: str = None) -> bool:
        """
        Check if attack is successful
        
        Args:
            code: Adversarial code
            target_output: Target output (optional)
            
        Returns:
            True if attack is successful, False otherwise
        """
        output = self.model(code)
        
        if target_output is not None:
            # For targeted attack
            return calculate_bleu(output, target_output) < self.similarity_threshold
        else:
            # For untargeted attack
            original_output = self.model(self.original_code)
            return calculate_bleu(output, original_output) < self.similarity_threshold
    
    def _is_valid_substitution(self, code: str) -> bool:
        """
        Check if a code substitution is valid
        
        Args:
            code: Candidate code
            
        Returns:
            True if the code is valid, False otherwise
        """
        try:
            # Try to compile the code
            compile(code, "<string>", "exec")
            return True
        except:
            return False 