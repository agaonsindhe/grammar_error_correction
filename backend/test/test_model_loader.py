import pytest

from backend.src.models.model_loader import load_model


def test_load_model():
    """
    Test if the model and tokenizer load correctly.
    """
    model_name = "agaonsindhe/grammar-error-correction-c2400m-t5-base"
    tokenizer, model = load_model(model_name)
    assert tokenizer is not None
    assert model is not None
