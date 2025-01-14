import pytest
from src.models.model_loader import load_model

def test_load_model():
    """
    Test if the model and tokenizer load correctly.
    """
    model_name = ""
    tokenizer, model = load_model(model_name)
    assert tokenizer is not None
    assert model is not None
