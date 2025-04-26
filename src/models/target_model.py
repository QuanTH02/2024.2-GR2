import numpy as np
import random

class TargetModel:
    def __init__(self, model_name="dummy"):
        self.model_name = model_name
        self.base_score = 0.7
        self.token_scores = {}
    
    def __call__(self, code):
        if "[MASK]" in code:
            return np.array([self.base_score - 0.2])
        else:
            tokens = code.split()
            for token in tokens:
                if token not in self.token_scores:
                    self.token_scores[token] = random.uniform(0.5, 0.9)
            return np.array([self.token_scores.get(tokens[0], self.base_score)]) 