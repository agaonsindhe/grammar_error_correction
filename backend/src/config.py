import os

# Flask Configuration
UPLOAD_FOLDER = "uploaded_files"
ALLOWED_EXTENSIONS = {"txt"}

# Model Configuration
MODEL_NAME = "agaonsindhe/grammar-error-correction-c2400m-t5-base"  # Change to your specific Hugging Face model if needed

# Logging Configuration
LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOGGING_LEVEL = "INFO"

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
