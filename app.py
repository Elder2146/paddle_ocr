import os
import logging
from io import BytesIO
from flask import Flask, request, jsonify, render_template, send_file
from pdf2image import convert_from_bytes
from paddleocr import PaddleOCR

# Initialize logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang="en")

# Initialize Flask app
app = Flask(__name__)

# Set upload folder
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Set Poppler path
POPPLER_PATH = r"C:\Users\useer\Desktop\paddle_ocr\ocr\poppler-24.08.0\Library\bin"  # Replace with your actual Poppler `bin` directory path

# Home route to render the upload form
@app.route("/")
def home():
    return render_template("index.html")

# Route to handle PDF upload and text extraction
@app.route("/extract-text", methods=["POST"])
def extract_text():
    try:
        # Check if a file is uploaded
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        # Check if the file is a PDF
        if file.filename == "" or not file.filename.lower().endswith(".pdf"):
            return jsonify({"error": "Invalid file type. Please upload a PDF file."}), 400

        # Save the uploaded file temporarily
        pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(pdf_path)

        # Convert PDF pages to images
        logging.info(f"Converting PDF to images...")
        pages = convert_from_bytes(
            open(pdf_path, "rb").read(), 
            dpi=200, 
            poppler_path=POPPLER_PATH
        )

        # Extract text from each page
        extracted_text = ""
        for index, page in enumerate(pages):
            logging.info(f"Processing page {index + 1}...")
            with BytesIO() as output_bytes:
                page.save(output_bytes, format="JPEG")
                output_bytes.seek(0)
                image_bytes = output_bytes.getvalue()

                # OCR processing
                ocr_result = ocr.ocr(image_bytes)

                # Append recognized text to the result
                for line in ocr_result[0]:
                    text = line[1][0]  # Extract recognized text
                    extracted_text += text + "\n"

                extracted_text += "\n" + "=" * 50 + "\n"  # Separator between pages

        # Save the extracted text to a file
        output_file = os.path.join(app.config["UPLOAD_FOLDER"], "extracted_text.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(extracted_text)

        # Return the extracted text as a response
        return jsonify({"extracted_text": extracted_text})

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

# Route to download the extracted text file
@app.route("/download-text")
def download_text():
    try:
        output_file = os.path.join(app.config["UPLOAD_FOLDER"], "extracted_text.txt")
        if not os.path.exists(output_file):
            return jsonify({"error": "No extracted text file found"}), 404

        return send_file(output_file, as_attachment=True, download_name="extracted_text.txt")

    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
