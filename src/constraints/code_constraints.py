from typing import List, Set
import re
from ..utils.tokenizer import CodeTokenizer

class CodeConstraints:
    def __init__(self):
        self.tokenizer = CodeTokenizer()
        
        self.keywords = {
            "java": {"public", "private", "protected", "static", "final", "class", "interface", 
                    "extends", "implements", "void", "int", "float", "double", "boolean", 
                    "char", "byte", "short", "long", "if", "else", "for", "while", "do", 
                    "switch", "case", "break", "continue", "return", "try", "catch", "finally", 
                    "throw", "throws", "new", "this", "super", "import", "package"},
            "python": {"def", "class", "if", "elif", "else", "for", "while", "try", "except", 
                      "finally", "with", "import", "from", "as", "pass", "break", "continue", 
                      "return", "yield", "raise", "global", "nonlocal", "True", "False", "None"},
            "csharp": {"public", "private", "protected", "internal", "static", "readonly", 
                      "class", "interface", "struct", "enum", "void", "int", "float", "double", 
                      "bool", "char", "byte", "short", "long", "if", "else", "for", "while", 
                      "do", "switch", "case", "break", "continue", "return", "try", "catch", 
                      "finally", "throw", "using", "namespace", "new", "this", "base"}
        }
        
        self.operator_constraints = {
            '+': ['-', '*', '/'],
            '-': ['+', '*', '/'],
            '*': ['+', '-', '/'],
            '/': ['+', '-', '*'],
            '++': ['--'],
            '--': ['++'],
            '==': ['!=', '>', '<', '>=', '<='],
            '!=': ['==', '>', '<', '>=', '<='],
            '>': ['<', '>=', '<=', '==', '!='],
            '<': ['>', '>=', '<=', '==', '!='],
            '>=': ['<=', '>', '<', '==', '!='],
            '<=': ['>=', '>', '<', '==', '!=']
        }
        
        self.bracket_constraints = {
            '(': [')'],
            '[': [']'],
            '{': ['}'],
            ')': ['('],
            ']': ['['],
            '}': ['{']
        }
        
    def filter_substitutes(self, original_token: str, substitutes: List[str]) -> List[str]:
        original_class = self._get_token_class(original_token)
        
        filtered_substitutes = []
        for substitute in substitutes:
            if substitute == original_token:
                continue
                
            substitute_class = self._get_token_class(substitute)
            
            if substitute_class != original_class:
                continue
                
            if original_class == "operator":
                if not self._check_operator_constraints(original_token, substitute):
                    continue
            
            if original_class == "bracket":
                if not self._check_bracket_constraints(original_token, substitute):
                    continue
            
            filtered_substitutes.append(substitute)
            
        return filtered_substitutes
    
    def _get_token_class(self, token: str) -> str:
        if token in self.operator_constraints:
            return 'operator'
        elif token in self.bracket_constraints:
            return 'bracket'
        elif token.isdigit():
            return 'number'
        elif token.isidentifier():
            return 'identifier'
        else:
            return 'unknown'
    
    def _check_operator_constraints(self, original: str, substitute: str) -> bool:
        if original not in self.operator_constraints:
            return False
        return substitute in self.operator_constraints[original]
    
    def _check_bracket_constraints(self, original: str, substitute: str) -> bool:
        if original not in self.bracket_constraints:
            return False
        return substitute in self.bracket_constraints[original] 