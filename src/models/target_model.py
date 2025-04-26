import numpy as np
import random

class TargetModel:
    def __init__(self, model_name="dummy"):
        self.model_name = model_name
        self.base_score = 0.7
        self.token_scores = {}
    
    def __call__(self, code):
        """Return a score based on code content"""
        # For testing purposes, return a score that varies based on code content
        if "[MASK]" in code:
            # Return a lower score for masked code
            return np.array([self.base_score - 0.2])
        else:
            # Return different scores for different tokens
            tokens = code.split()
            for token in tokens:
                if token not in self.token_scores:
                    self.token_scores[token] = random.uniform(0.5, 0.9)
            return np.array([self.token_scores.get(tokens[0], self.base_score)]) 