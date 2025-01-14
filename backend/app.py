import logging
import os
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, send_from_directory,send_file
from flask_cors import CORS
from src.config import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, MODEL_NAME
from src.utils.file_utils import allowed_file, save_corrected_file
from src.utils.grammar_utils import correct_grammar
from src.models.model_loader import load_model

# Configure logging
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger()

# Initialize Flask app
app = Flask(__name__, static_folder="../static", template_folder="../../static")
CORS(app)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# Load the model
tokenizer, model = load_model(MODEL_NAME)


@app.route("/index", methods=["GET"])
def home():
    """
    Serve the frontend HTML page.
    """
    logger.info("Home endpoint accessed.")
    return send_from_directory(app.static_folder,'index.html')


@app.route("/correct_text", methods=["POST"])
def correct_text():
    """
    Endpoint to correct grammar for input text.
    """
    try:
        data = request.json
        if "text" not in data:
            return jsonify({"error": "No text provided"}), 400

        input_text = data["text"]
        corrected_text = correct_grammar(input_text, tokenizer, model)
        return jsonify({"original_text": input_text, "corrected_text": corrected_text})

    except Exception as e:
        logger.error(f"Error during text correction: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/upload_file", methods=["POST"])
def upload_file():
    """
    Endpoint to correct grammar for uploaded files.
    """
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file part"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if allowed_file(file.filename, ALLOWED_EXTENSIONS):
            print(file.filename)
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            logger.debug(filepath)
            file.save(filepath)

            # Read and process the file line by line
            corrected_lines = []
            with open(filepath, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:  # Ignore empty lines
                        corrected_line = correct_grammar(line,tokenizer, model)
                        corrected_lines.append(corrected_line)

            # Join corrected lines
            corrected_content = "\n".join(corrected_lines)
            print(corrected_content)
            logger.debug(corrected_content)
            print(os.path.abspath(app.config["UPLOAD_FOLDER"]))
            corrected_filepath = save_corrected_file(corrected_content, file.filename, UPLOAD_FOLDER)
            return jsonify({"corrected_file_url": f"http://127.0.0.1:5000/uploaded_files/{corrected_filepath.split('/')[-1]}"})

        return jsonify({"error": "Invalid file type"}), 400

    except Exception as e:
        logger.error(f"Error during file upload: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/uploaded_files/<filename>")
def serve_file(filename):
    """
    Serve corrected files for download.
    """
    try:
        # Use send_from_directory to serve files safely
        print(os.path.abspath(app.config["UPLOAD_FOLDER"]))
        print(filename)
        return send_from_directory(os.path.abspath(app.config["UPLOAD_FOLDER"]), filename, as_attachment=True)
    except Exception as e:
        logger.error(f"Error serving file: {e}")
        return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
