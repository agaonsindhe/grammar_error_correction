# Grammar Error Correction

This project is a **Grammar Error Correction Application** designed to correct grammatical errors in text inputs and uploaded files. It utilizes the **google/t5-base model**, trained and fine-tuned on a Kaggle dataset, with the fine-tuned model hosted on the Hugging Face repository.

---

## **Project Structure**

```
grammar_error_correction/
├── backend/
│   ├── app.log                  # Log file for backend operations
│   ├── app.py                   # Flask backend application
│   ├── requirements.txt         # Backend Python dependencies
│   ├── uploaded_files/          # Directory for storing uploaded and corrected files
├── static/
│   ├── css/
│   │   └── style.css            # Stylesheet for frontend UI
│   ├── js/
│   │   └── app.js               # JavaScript logic for frontend interactions
│   └── index.html               # Frontend HTML file
├── uploaded_files/              # Additional storage for file processing
├── venv-gca/                    # Virtual environment for Python dependencies
├── app.log                      # General log file
├── run.sh                       # Script to start the backend server
└── read.me                      # This README file
```

---

## **Features**

### **Frontend**
- Simple, responsive UI for:
  - **Text input**: Manually input text for grammar correction.
  - **File upload**: Upload `.txt` files for batch grammar correction.
- Styled with CSS for clarity and user-friendliness.
- Interacts seamlessly with the backend API.

### **Backend**
- Flask-based backend API with the following endpoints:
  - **`/correct_text`**: Accepts text input and returns the corrected version.
  - **`/upload_file`**: Processes uploaded `.txt` files and returns corrected versions.
  - **`/uploaded_files/<filename>`**: Serves corrected files for download.
- Grammar correction powered by the **google/t5-base model**, fine-tuned for grammar correction tasks.
- Logs backend operations in `app.log`.

### **Model**
- **google/t5-base**:
  - Pre-trained on a large corpus and fine-tuned on a Kaggle dataset for grammar correction tasks.
  - Hosted on Hugging Face for reuse and deployment.

### **Dataset**
- The model was fine-tuned using the Kaggle dataset [C4_200M Synthetic Dataset for Grammatical Error Correction](https://www.kaggle.com/datasets/a0155991rliwei/c4-200m).

---

## **Setup and Installation**

### **1. Clone the Repository**
```bash
git clone <repository_url>
cd grammar_error_correction
```

### **2. Create and Activate a Virtual Environment**
```bash
python3 -m venv backend/venv-gca
source backend/venv-gca/bin/activate
```

### **3. Install Backend Dependencies**
```bash
pip install -r backend/requirements.txt
```

### **4. Start the Backend Server**
Use the provided `run.sh` script:
```bash
chmod +x run.sh
./run.sh
```

Alternatively, you can start the server manually:
```bash
python backend/app.py
```

### **5. Open the Frontend**
Open the `static/index.html` file in any modern browser to access the application.

---

## **How to Use**

### **1. Correct Text**
1. Enter text in the text box.
2. Click the "Correct Text" button.
3. The corrected text will be displayed on the screen.

### **2. Correct Uploaded Files**
1. Upload a `.txt` file.
2. Click the "Upload File" button.
3. Download the corrected file from the provided link.

---

## **API Endpoints**

### **1. `/correct_text`**
- **Method**: POST
- **Request Body**:
  ```json
  {
      "text": "This is a bad sentense."
  }
  ```
- **Response**:
  ```json
  {
      "original_text": "This is a bad sentense.",
      "corrected_text": "This is a bad sentence."
  }
  ```

### **2. `/upload_file`**
- **Method**: POST
- **Request Body**: Multipart form data with the file to be uploaded.
- **Response**:
  ```json
  {
      "original_file": "input.txt",
      "corrected_file_url": "http://127.0.0.1:5000/uploaded_files/input_corrected.txt"
  }
  ```

### **3. `/uploaded_files/<filename>`**
- Serves corrected files for download.

---

## **Dependencies**
- Flask
- Flask-CORS
- Transformers
- Torch
- SentencePiece

Install them via:
```bash
pip install -r backend/requirements.txt
```

---

## **Logging**
- Backend logs are written to `backend/app.log`.

---

## **Future Enhancements**
1. **Multilingual Grammar Correction**:
   - Extend the model to support multiple languages.
2. **Enhanced UI**:
   - Add progress bars for file uploads and improved responsiveness.
3. **Cloud Deployment**:
   - Deploy the application on cloud platforms like AWS or Azure.

---
