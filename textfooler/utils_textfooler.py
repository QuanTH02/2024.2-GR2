# Simple stub implementation for textfooler utils
# This is a minimal implementation to resolve import errors

def get_var():
    """
    Stub implementation for get_var.
    Returns empty dictionaries and None for the required variables.
    """
    print("Warning: TextFooler get_var functionality is not implemented. Using stub.")
    return {}, {}, None

def get_sim_predictor():
    """
    Stub implementation for similarity predictor.
    Returns a simple object with a semantic_sim method that always returns 1.0.
    """
    class StubSimPredictor:
        def semantic_sim(self, texts1, texts2):
            """
            Stub semantic similarity method.
            Returns 1.0 (maximum similarity) for all text pairs.
            """
            return [1.0] * len(texts1)
    
    print("Warning: TextFooler similarity predictor is not implemented. Using stub.")
    return StubSimPredictor() 