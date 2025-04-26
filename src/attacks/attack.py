import torch
import numpy as np
from typing import Dict, Any, List
from transformers import PreTrainedModel, PreTrainedTokenizer
from src.utils.metrics import calculate_similarity
import ast

class CodeAttack:
    def __init__(
        self,
        model: PreTrainedModel,
        tokenizer: PreTrainedTokenizer,
        max_perturbations: float = 0.4,
        similarity_threshold: float = 0.5
    ):
        self.model = model
        self.tokenizer = tokenizer
        self.max_perturbations = max_perturbations
        self.similarity_threshold = similarity_threshold
        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self.model.to(self.device)
        
        self.token_substitutes = {
            '+': ['-', '*', '/'],
            '-': ['+', '*', '/'],
            '*': ['+', '-', '/'],
            '/': ['+', '-', '*'],
            'if': ['elif', 'while'],
            'elif': ['if', 'while'],
            'while': ['if', 'elif'],
            'return': ['yield', 'print'],
            'yield': ['return', 'print'],
            'print': ['return', 'yield']
        }
        
        self.insertion_tokens = [
            'if True:',
            'if False:',
            'pass',
            'continue',
            'break',
            'return None',
            'print("")',
            'yield None'
        ]
    
    def find_vulnerable_tokens(self, code: str) -> List[Dict[str, Any]]:
        tokens = self.tokenizer.tokenize(code)
        
        inputs = self.tokenizer(code, return_tensors='pt')
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            embeddings = self.model.get_input_embeddings()(inputs['input_ids'])
            output = self.model.generate(**inputs)
        
        importance_scores = self._calculate_token_importance(embeddings, output)
        
        vulnerable_tokens = []
        for i, token in enumerate(tokens):
            if importance_scores[i] > 0.5:
                vulnerable_tokens.append({
                    'token': token,
                    'position': i,
                    'influence_score': float(importance_scores[i])
                })
        
        vulnerable_tokens.sort(key=lambda x: x['influence_score'], reverse=True)
        
        return vulnerable_tokens
    
    def generate_substitutes(self, token: str, context: str) -> List[str]:
        token_type = self._get_token_type(token)
        
        if token_type == 'operator':
            return self.token_substitutes.get(token, [])
        elif token_type == 'identifier':
            return [f"{token}_new", f"new_{token}", f"{token}1"]
        elif token_type == 'number':
            try:
                num = int(token)
                return [str(num + 1), str(num - 1), str(num * 2)]
            except ValueError:
                return []
        else:
            return []
    
    def _get_token_type(self, token: str) -> str:
        if token in self.token_substitutes:
            return 'operator'
        elif token.isidentifier():
            return 'identifier'
        elif token.isdigit():
            return 'number'
        else:
            return 'unknown'
    
    def generate(self, code: str) -> Dict[str, Any]:
        if not self._is_valid_code(code):
            return {
                'original_code': code,
                'adversarial_code': code,
                'perturbations': 0,
                'similarity': 1.0
            }
        
        inputs = self.tokenizer(code, return_tensors='pt')
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        with torch.no_grad():
            original_output = self.model.generate(**inputs)
        
        adversarial_code = self._generate_adversarial(code, inputs, original_output)
        
        perturbations = self._count_perturbations(code, adversarial_code)
        similarity = calculate_similarity(code, adversarial_code)
        
        return {
            'original_code': code,
            'adversarial_code': adversarial_code,
            'perturbations': perturbations,
            'similarity': similarity
        }
    
    def _generate_adversarial(
        self,
        code: str,
        inputs: Dict[str, torch.Tensor],
        original_output: torch.Tensor
    ) -> str:
        methods = [
            self._token_substitution,
            self._token_insertion,
            self._token_deletion,
            self._token_reordering
        ]
        
        best_adversarial = code
        best_similarity = 1.0
        
        for method in methods:
            try:
                adversarial = method(code, inputs, original_output)
                if adversarial == code:
                    continue
                    
                similarity = calculate_similarity(code, adversarial)
                
                if similarity >= self.similarity_threshold and similarity < best_similarity:
                    best_adversarial = adversarial
                    best_similarity = similarity
            except Exception as e:
                print(f"Error in {method.__name__}: {str(e)}")
                continue
        
        return best_adversarial
    
    def _token_substitution(
        self,
        code: str,
        inputs: Dict[str, torch.Tensor],
        original_output: torch.Tensor
    ) -> str:
        with torch.no_grad():
            embeddings = self.model.get_input_embeddings()(inputs['input_ids'])
        
        importance_scores = self._calculate_token_importance(embeddings, original_output)
        
        tokens = self.tokenizer.tokenize(code)
        for i in range(len(tokens)):
            if i < len(importance_scores) and importance_scores[i] > 0.5:
                for substitute in self._get_token_substitutes(tokens[i]):
                    new_tokens = tokens.copy()
                    new_tokens[i] = substitute
                    new_code = self.tokenizer.convert_tokens_to_string(new_tokens)
                    
                    if self._is_valid_code(new_code):
                        return new_code
        
        return code
    
    def _token_insertion(
        self,
        code: str,
        inputs: Dict[str, torch.Tensor],
        original_output: torch.Tensor
    ) -> str:
        with torch.no_grad():
            embeddings = self.model.get_input_embeddings()(inputs['input_ids'])
        
        insertion_scores = self._calculate_insertion_scores(embeddings, original_output)
        
        tokens = self.tokenizer.tokenize(code)
        for i in range(len(tokens)):
            if i < len(insertion_scores) and insertion_scores[i] > 0.5:
                for token_to_insert in self._get_insertion_tokens():
                    new_tokens = tokens.copy()
                    new_tokens.insert(i, token_to_insert)
                    new_code = self.tokenizer.convert_tokens_to_string(new_tokens)
                    
                    if self._is_valid_code(new_code):
                        return new_code
        
        return code
    
    def _token_deletion(
        self,
        code: str,
        inputs: Dict[str, torch.Tensor],
        original_output: torch.Tensor
    ) -> str:
        with torch.no_grad():
            embeddings = self.model.get_input_embeddings()(inputs['input_ids'])
        
        deletion_scores = self._calculate_deletion_scores(embeddings, original_output)
        
        tokens = self.tokenizer.tokenize(code)
        for i in range(len(tokens)):
            if i < len(deletion_scores) and deletion_scores[i] > 0.5:
                new_tokens = tokens.copy()
                del new_tokens[i]
                new_code = self.tokenizer.convert_tokens_to_string(new_tokens)
                
                if self._is_valid_code(new_code):
                    return new_code
        
        return code
    
    def _token_reordering(
        self,
        code: str,
        inputs: Dict[str, torch.Tensor],
        original_output: torch.Tensor
    ) -> str:
        with torch.no_grad():
            embeddings = self.model.get_input_embeddings()(inputs['input_ids'])
        
        reordering_scores = self._calculate_reordering_scores(embeddings, original_output)
        
        tokens = self.tokenizer.tokenize(code)
        for i in range(len(tokens) - 1):
            if i < len(reordering_scores) and reordering_scores[i] > 0.5:
                new_tokens = tokens.copy()
                new_tokens[i], new_tokens[i + 1] = new_tokens[i + 1], new_tokens[i]
                new_code = self.tokenizer.convert_tokens_to_string(new_tokens)
                
                if self._is_valid_code(new_code):
                    return new_code
        
        return code
    
    def _calculate_token_importance(
        self,
        embeddings: torch.Tensor,
        original_output: torch.Tensor
    ) -> np.ndarray:
        embeddings.requires_grad = True
        output = self.model(inputs_embeds=embeddings, decoder_input_ids=original_output)
        
        if output.loss is None:
            logits = output.logits
            labels = original_output
            loss_fn = torch.nn.CrossEntropyLoss()
            loss = loss_fn(logits.view(-1, logits.size(-1)), labels.view(-1))
        else:
            loss = output.loss
            
        if not loss.requires_grad:
            loss = loss.clone().detach().requires_grad_(True)
            
        loss.backward()
        
        if embeddings.grad is None:
            return np.zeros(embeddings.size(0))
            
        importance_scores = torch.abs(embeddings.grad).mean(dim=-1)
        importance_scores = importance_scores.cpu().numpy()
        
        if importance_scores.size > 0:
            importance_scores = (importance_scores - importance_scores.min()) / (importance_scores.max() - importance_scores.min() + 1e-8)
        
        return importance_scores
    
    def _calculate_insertion_scores(
        self,
        embeddings: torch.Tensor,
        original_output: torch.Tensor
    ) -> np.ndarray:
        importance_scores = self._calculate_token_importance(embeddings, original_output)
        insertion_scores = np.zeros(len(importance_scores) + 1)
        insertion_scores[1:-1] = (importance_scores[:-1] + importance_scores[1:]) / 2
        insertion_scores[0] = importance_scores[0]
        insertion_scores[-1] = importance_scores[-1]
        
        return insertion_scores
    
    def _calculate_deletion_scores(
        self,
        embeddings: torch.Tensor,
        original_output: torch.Tensor
    ) -> np.ndarray:
        return self._calculate_token_importance(embeddings, original_output)
    
    def _calculate_reordering_scores(
        self,
        embeddings: torch.Tensor,
        original_output: torch.Tensor
    ) -> np.ndarray:
        importance_scores = self._calculate_token_importance(embeddings, original_output)
        reordering_scores = np.zeros(len(importance_scores) - 1)
        reordering_scores = (importance_scores[:-1] + importance_scores[1:]) / 2
        
        return reordering_scores
    
    def _get_token_substitutes(self, token: str) -> List[str]:
        return self.token_substitutes.get(token, [])
    
    def _get_insertion_tokens(self) -> List[str]:
        return self.insertion_tokens
    
    def _is_valid_code(self, code: str) -> bool:
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False
    
    def _count_perturbations(self, original_code: str, adversarial_code: str) -> int:
        original_tokens = self.tokenizer.tokenize(original_code)
        adversarial_tokens = self.tokenizer.tokenize(adversarial_code)
        
        from Levenshtein import distance
        return distance(original_tokens, adversarial_tokens) 