import pytest
from src.attack.attack import CodeAttack
from src.constraints.code_constraints import CodeConstraints
from src.utils.tokenizer import CodeTokenizer

class MockModel:
    def __init__(self):
        self.original_code = None
        
    def __call__(self, code):
        if self.original_code is None:
            self.original_code = code
            return 1.0
        return 0.5

@pytest.fixture
def mock_model():
    return MockModel()

@pytest.fixture
def code_attack(mock_model):
    return CodeAttack(
        model=mock_model,
        max_perturbations=0.4,
        similarity_threshold=0.5
    )

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