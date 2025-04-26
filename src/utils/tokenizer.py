from typing import List
import re

class CodeTokenizer:
    def __init__(self):
        self.patterns = {
            "keyword": r"\b(public|private|protected|static|final|class|interface|extends|implements|void|int|float|double|boolean|char|byte|short|long|if|else|for|while|do|switch|case|break|continue|return|try|catch|finally|throw|throws|new|this|super|import|package)\b",
            "operator": r"(\+\+|--|\+=|-=|\*=|\/=|%=|&=|\|=|\^=|<<=|>>=|==|!=|<=|>=|&&|\|\||!|&|\||\^|~|<<|>>|\+|-|\*|\/|%|=|<|>)",
            "bracket": r"([\(\)\{\}\[\]])",
            "number": r"\b\d+(\.\d+)?\b",
            "string": r'"[^"]*"|\'[^\']*\'',
            "identifier": r"\b[a-zA-Z_][a-zA-Z0-9_]*\b"
        }
        
    def tokenize(self, code: str) -> List[str]:
        tokens = []
        current_pos = 0
        
        while current_pos < len(code):
            if code[current_pos].isspace():
                current_pos += 1
                continue
                
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
                tokens.append(code[current_pos])
                current_pos += 1
                
        return tokens
    
    def get_token_type(self, token: str) -> str:
        for token_type, pattern in self.patterns.items():
            if re.fullmatch(pattern, token):
                return token_type
                
        return "unknown"
    
    def is_valid_identifier(self, token: str) -> bool:
        return bool(re.fullmatch(self.patterns["identifier"], token))
    
    def is_valid_number(self, token: str) -> bool:
        return bool(re.fullmatch(self.patterns["number"], token))
    
    def is_valid_string(self, token: str) -> bool:
        return bool(re.fullmatch(self.patterns["string"], token)) 