import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from transformers import T5Tokenizer

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,  # Set to INFO or WARNING in production
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration for file uploads
UPLOAD_FOLDER = "uploaded_files"
ALLOWED_EXTENSIONS = {"txt"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize the grammar correction model
try:
    MODEL_NAME = "thenHung/english-grammar-error-correction-t5-seq2seq"
    tokenizer = T5Tokenizer.from_pretrained(MODEL_NAME)

    model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
    logger.info("Pretrained grammar correction model loaded successfully.")
except Exception as e:
    logger.critical(f"Failed to initialize the pretrained model: {e}")
    raise e

# Helper function to check allowed file types
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Grammar correction function
def correct_grammar(input_text):
    try:
        inputs = tokenizer(input_text, return_tensors="pt", truncation=True, padding=True)
        outputs = model.generate(inputs["input_ids"])
        corrected_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return corrected_text
    except Exception as e:
        logger.error(f"Error during grammar correction: {e}")
        raise e

# Home route for testing
@app.route("/", methods=["GET"])
def home():
    logger.info("Home endpoint accessed.")
    return "Grammar Correction API is Running with Pretrained Models!"

# Endpoint to correct text input
@app.route("/correct_text", methods=["POST"])
def correct_text():
    try:
        data = request.json
        if "text" not in data:
            logger.warning("No text provided in the request.")
            return jsonify({"error": "No text provided"}), 400

        input_text = data["text"]
        corrected_text = correct_grammar(input_text)

        logger.info("Text correction successful.")
        return jsonify({
            "original_text": input_text,
            "corrected_text": corrected_text,
        })

    except Exception as e:
        logger.error(f"Error during text correction: {e}")
        return jsonify({"error": "An internal error occurred"}), 500

# Endpoint to handle file uploads
@app.route("/upload_file", methods=["POST"])
def upload_file():
    try:
        if "file" not in request.files:
            logger.warning("No file part in the request.")
            return jsonify({"error": "No file part"}), 400

        file = request.files["file"]
        if file.filename == "":
            logger.warning("No file selected for upload.")
            return jsonify({"error": "No selected file"}), 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            # Read and process the file line by line
            corrected_lines = []
            with open(filepath, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:  # Ignore empty lines
                        corrected_line = correct_grammar(line)
                        corrected_lines.append(corrected_line)

            # Join corrected lines
            corrected_content = "\n".join(corrected_lines)

            # Save corrected content to a new file
            corrected_filename = filename.replace(".txt", "_corrected.txt")
            corrected_filepath = os.path.join(app.config["UPLOAD_FOLDER"], corrected_filename)
            with open(corrected_filepath, "w") as f:
                f.write(corrected_content)

            logger.info(f"File correction successful. Original: {filename}, Corrected: {corrected_filepath}")
            # Return the URL for the corrected file
            corrected_file_url = f"http://127.0.0.1:5000/uploaded_files/{corrected_filename}"
            return jsonify({
                "original_file": filename,
                "corrected_file_url": corrected_file_url,
            })

        logger.warning("Invalid file type uploaded.")
        return jsonify({"error": "Invalid file type"}), 400

    except Exception as e:
        logger.error(f"Error during file processing: {e}")
        return jsonify({"error": "An internal error occurred"}), 500


from flask import send_from_directory

@app.route("/uploaded_files/<filename>")
def serve_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# Run the Flask app
if __name__ == "__main__":
    try:
        logger.info("Starting Flask server...")
        app.run(debug=True)
    except Exception as e:
        logger.critical(f"Failed to start Flask server: {e}")
        raise e
