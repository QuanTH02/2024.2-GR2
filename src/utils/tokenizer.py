from typing import List
import re

class CodeTokenizer:
    def __init__(self):
        """Initialize code tokenizer"""
        # Define patterns for different token types
        self.patterns = {
            "keyword": r"\b(public|private|protected|static|final|class|interface|extends|implements|void|int|float|double|boolean|char|byte|short|long|if|else|for|while|do|switch|case|break|continue|return|try|catch|finally|throw|throws|new|this|super|import|package)\b",
            "operator": r"(\+\+|--|\+=|-=|\*=|\/=|%=|&=|\|=|\^=|<<=|>>=|==|!=|<=|>=|&&|\|\||!|&|\||\^|~|<<|>>|\+|-|\*|\/|%|=|<|>)",
            "bracket": r"([\(\)\{\}\[\]])",
            "number": r"\b\d+(\.\d+)?\b",
            "string": r'"[^"]*"|\'[^\']*\'',
            "identifier": r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"
        }
        
    def tokenize(self, code: str) -> List[str]:
        """
        Tokenize code into tokens
        
        Args:
            code: Input code snippet
            
        Returns:
            List of tokens
        """
        tokens = []
        current_pos = 0
        
        while current_pos < len(code):
            # Skip whitespace
            if code[current_pos].isspace():
                current_pos += 1
                continue
                
            # Try to match each pattern
            matched = False
            for pattern in self.patterns.values():
                match = re.match(pattern, code[current_pos:])
                if match:
                    token = match.group(0)
                    tokens.append(token)
                    current_pos += len(token)
                    matched = True
                    break
                    
            if not matched:
                # If no pattern matched, take next character as token
                tokens.append(code[current_pos])
                current_pos += 1
                
        return tokens
    
    def get_token_type(self, token: str) -> str:
        """
        Get the type of a token
        
        Args:
            token: Input token
            
        Returns:
            Token type (keyword, operator, bracket, number, string, or identifier)
        """
        for token_type, pattern in self.patterns.items():
            if re.fullmatch(pattern, token):
                return token_type
                
        return "unknown"
    
    def is_valid_identifier(self, token: str) -> bool:
        """
        Check if a token is a valid identifier
        
        Args:
            token: Input token
            
        Returns:
            True if token is a valid identifier, False otherwise
        """
        return bool(re.fullmatch(self.patterns["identifier"], token))
    
    def is_valid_number(self, token: str) -> bool:
        """
        Check if a token is a valid number
        
        Args:
            token: Input token
            
        Returns:
            True if token is a valid number, False otherwise
        """
        return bool(re.fullmatch(self.patterns["number"], token))
    
    def is_valid_string(self, token: str) -> bool:
        """
        Check if a token is a valid string
        
        Args:
            token: Input token
            
        Returns:
            True if token is a valid string, False otherwise
        """
        return bool(re.fullmatch(self.patterns["string"], token)) 