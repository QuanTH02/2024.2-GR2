import pytest
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from src.attacks.attack import CodeAttack
from src.constraints.code_constraints import CodeConstraints
from src.utils.tokenizer import CodeTokenizer

class MockModel:
    def __init__(self):
        self.original_code = None
        
    def __call__(self, **kwargs):
        if 'inputs_embeds' in kwargs:
            return type('obj', (object,), {
                'loss': torch.tensor(0.5),
                'logits': torch.randn(1, 10, 768)
            })
        return 0.5
        
    def get_input_embeddings(self):
        return lambda x: torch.randn(x.shape[0], x.shape[1], 768)
        
    def generate(self, **kwargs):
        return torch.randn(1, 10)
        
    def to(self, device):
        return self

@pytest.fixture
def mock_model():
    return MockModel()

@pytest.fixture
def mock_tokenizer():
    tokenizer = AutoTokenizer.from_pretrained("Salesforce/codet5-base")
    return tokenizer

@pytest.fixture
def code_attack(mock_model, mock_tokenizer):
    return CodeAttack(
        model=mock_model,
        tokenizer=mock_tokenizer,
        max_perturbations=0.4,
        similarity_threshold=0.5
    )

@pytest.fixture
def model_and_tokenizer():
    model_name = "Salesforce/codet5-base"
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return model, tokenizer

@pytest.fixture
def attack(model_and_tokenizer):
    model, tokenizer = model_and_tokenizer
    return CodeAttack(model=model, tokenizer=tokenizer)

def test_find_vulnerable_tokens(code_attack):
    code = """
    public class Test {
        public static void main(String[] args) {
            int x = 10;
            System.out.println(x);
        }
    }
    """
    
    vulnerable_tokens = code_attack.find_vulnerable_tokens(code)
    
    # Check that tokens are found
    assert len(vulnerable_tokens) > 0
    
    # Check that tokens are sorted by influence score
    scores = [token["influence_score"] for token in vulnerable_tokens]
    assert scores == sorted(scores, reverse=True)

def test_generate_substitutes(code_attack):
    token = "x"
    context = "int x = 10;"
    
    substitutes = code_attack.generate_substitutes(token, context)
    
    # Check that substitutes are generated
    assert len(substitutes) > 0
    
    # Check that substitutes are valid identifiers
    tokenizer = CodeTokenizer()
    assert all(tokenizer.is_valid_identifier(sub) for sub in substitutes)

def test_generate_adversarial_example(code_attack):
    code = """
    public class Test {
        public static void main(String[] args) {
            int x = 10;
            System.out.println(x);
        }
    }
    """
    
    result = code_attack.generate(code)
    
    # Check that adversarial example is generated
    assert "adversarial_code" in result
    assert result["adversarial_code"] != code
    
    # Check that number of perturbations is within limit
    max_perturbations = int(len(code.split()) * 0.4)
    assert result["perturbations"] <= max_perturbations
    
    # Check that similarity meets threshold
    assert result["similarity"] >= 0.5

def test_code_constraints():
    constraints = CodeConstraints()
    
    # Test operator constraints
    assert constraints._check_operator_constraints("+", "-")
    assert not constraints._check_operator_constraints("+", "++")
    
    # Test bracket constraints
    assert constraints._check_bracket_constraints("(", "{")
    assert not constraints._check_bracket_constraints("(", ")")
    
    # Test token class identification
    assert constraints._get_token_class("public") == "keyword"
    assert constraints._get_token_class("+") == "operator"
    assert constraints._get_token_class("(") == "bracket"
    assert constraints._get_token_class("123") == "argument"
    assert constraints._get_token_class("variable") == "identifier"

def test_tokenizer():
    tokenizer = CodeTokenizer()
    
    # Test tokenization
    code = "int x = 10;"
    tokens = tokenizer.tokenize(code)
    assert tokens == ["int", "x", "=", "10", ";"]
    
    # Test token type identification
    assert tokenizer.get_token_type("int") == "keyword"
    assert tokenizer.get_token_type("x") == "identifier"
    assert tokenizer.get_token_type("=") == "operator"
    assert tokenizer.get_token_type("10") == "number"
    assert tokenizer.get_token_type(";") == "unknown"
    
    # Test validation functions
    assert tokenizer.is_valid_identifier("variable")
    assert not tokenizer.is_valid_identifier("123")
    assert tokenizer.is_valid_number("123")
    assert not tokenizer.is_valid_number("abc")
    assert tokenizer.is_valid_string('"test"')
    assert not tokenizer.is_valid_string("test")

def test_token_substitution(attack):
    code = "def add(a, b): return a + b"
    result = attack.generate(code)
    assert result['original_code'] == code
    assert result['adversarial_code'] != code
    assert result['similarity'] >= 0.5
    assert result['perturbations'] > 0

def test_token_insertion(attack):
    code = "def multiply(x, y): return x * y"
    result = attack.generate(code)
    assert result['original_code'] == code
    assert result['adversarial_code'] != code
    assert result['similarity'] >= 0.5
    assert result['perturbations'] > 0

def test_token_deletion(attack):
    code = "def divide(a, b): return a / b"
    result = attack.generate(code)
    assert result['original_code'] == code
    assert result['adversarial_code'] != code
    assert result['similarity'] >= 0.5
    assert result['perturbations'] > 0

def test_token_reordering(attack):
    code = "def subtract(a, b): return a - b"
    result = attack.generate(code)
    assert result['original_code'] == code
    assert result['adversarial_code'] != code
    assert result['similarity'] >= 0.5
    assert result['perturbations'] > 0

def test_invalid_code(attack):
    code = "def invalid(): return"
    result = attack.generate(code)
    assert result['original_code'] == code
    assert result['adversarial_code'] == code  # Should not modify invalid code
    assert result['similarity'] == 1.0
    assert result['perturbations'] == 0

def test_empty_code(attack):
    code = ""
    result = attack.generate(code)
    assert result['original_code'] == code
    assert result['adversarial_code'] == code  # Should not modify empty code
    assert result['similarity'] == 1.0
    assert result['perturbations'] == 0

def test_long_code(attack):
    code = """
    def complex_function(a, b, c):
        if a > b:
            return a + c
        elif b > c:
            return b - a
        else:
            return c * b
    """
    result = attack.generate(code)
    assert result['original_code'] == code
    assert result['adversarial_code'] != code
    assert result['similarity'] >= 0.5
    assert result['perturbations'] > 0 