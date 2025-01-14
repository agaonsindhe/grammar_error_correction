from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import logging

# Configure logging
logger = logging.getLogger(__name__)

def load_model(model_name: str):
    """
    Load the grammar correction model and tokenizer.

    Args:
        model_name (str): Name of the pre-trained model.

    Returns:
        tuple: tokenizer, model
    """
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        logger.info(f"Model '{model_name}' loaded successfully.")
        return tokenizer, model
    except Exception as e:
        logger.critical(f"Failed to load the model '{model_name}': {e}")
        raise e
