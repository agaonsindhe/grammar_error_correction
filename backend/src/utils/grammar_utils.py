
def correct_grammar(input_text: str, tokenizer, model) -> str:
    """
    Perform grammar correction on the input text.

    Args:
        input_text (str): The text to correct.
        tokenizer: Tokenizer for the model.
        model: Pre-trained grammar correction model.

    Returns:
        str: Corrected text.
    """
    try:
        inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True)
        outputs = model.generate(inputs["input_ids"])
        corrected_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return corrected_text
    except Exception as e:
        raise RuntimeError(f"Error during grammar correction: {e}")
