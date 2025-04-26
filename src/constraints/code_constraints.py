from typing import List, Set
import re
from ..utils.tokenizer import CodeTokenizer

class CodeConstraints:
    def __init__(self):
        """Initialize code-specific constraints"""
        self.tokenizer = CodeTokenizer()
        
        # Define token classes
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
        
        self.operators = {"+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">=", 
                         "&&", "||", "!", "&", "|", "^", "~", "<<", ">>", "++", "--", "+=", 
                         "-=", "*=", "/=", "%=", "&=", "|=", "^=", "<<=", ">>="}
        
        self.brackets = {"(", ")", "{", "}", "[", "]"}
        
    def filter_substitutes(self, original_token: str, substitutes: List[str]) -> List[str]:
        """
        Filter substitute tokens based on code-specific constraints
        
        Args:
            original_token: Original token to be replaced
            substitutes: List of potential substitute tokens
            
        Returns:
            Filtered list of valid substitute tokens
        """
        # Get token class of original token
        original_class = self._get_token_class(original_token)
        
        filtered_substitutes = []
        for substitute in substitutes:
            # Skip if substitute is same as original
            if substitute == original_token:
                continue
                
            # Get token class of substitute
            substitute_class = self._get_token_class(substitute)
            
            # Check if classes match
            if substitute_class != original_class:
                continue
                
            # Check operator constraints
            if original_class == "operator":
                if not self._check_operator_constraints(original_token, substitute):
                    continue
            
            # Check bracket constraints
            if original_class == "bracket":
                if not self._check_bracket_constraints(original_token, substitute):
                    continue
            
            filtered_substitutes.append(substitute)
            
        return filtered_substitutes
    
    def _get_token_class(self, token: str) -> str:
        """
        Get the class of a token
        
        Args:
            token: Input token
            
        Returns:
            Token class (keyword, identifier, operator, bracket, or argument)
        """
        # Check if keyword
        for lang_keywords in self.keywords.values():
            if token in lang_keywords:
                return "keyword"
                
        # Check if operator
        if token in self.operators:
            return "operator"
            
        # Check if bracket
        if token in self.brackets:
            return "bracket"
            
        # Check if argument (number or string)
        if re.match(r'^-?\d+(\.\d+)?$', token) or (token.startswith('"') and token.endswith('"')) or \
           (token.startswith("'") and token.endswith("'")):
            return "argument"
            
        # Default to identifier
        return "identifier"
    
    def _check_operator_constraints(self, original: str, substitute: str) -> bool:
        """
        Check operator-specific constraints
        
        Args:
            original: Original operator
            substitute: Substitute operator
            
        Returns:
            True if constraints are satisfied, False otherwise
        """
        # Count number of characters
        if abs(len(original) - len(substitute)) > 1:
            return False
            
        # Check if both are assignment operators
        if original.endswith("=") != substitute.endswith("="):
            return False
            
        return True
    
    def _check_bracket_constraints(self, original: str, substitute: str) -> bool:
        """
        Check bracket-specific constraints
        
        Args:
            original: Original bracket
            substitute: Substitute bracket
            
        Returns:
            True if constraints are satisfied, False otherwise
        """
        # Check if both are opening or both are closing brackets
        opening_brackets = {"(", "{", "["}
        if (original in opening_brackets) != (substitute in opening_brackets):
            return False
            
        return True 