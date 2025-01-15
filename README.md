PaddleOCR PDF Text Extraction App:
This project is a Flask-based web application that uses PaddleOCR and pdf2image to extract text from PDF documents. It provides a simple interface for users to upload PDFs, process them, and extract text using OCR (Optical Character Recognition). The application also supports downloading the extracted text as a .txt file.

Features:
Upload PDF Files: Upload a PDF document through the web interface.
Text Extraction: Extract text from each page of the PDF using PaddleOCR.
Poppler Integration: Uses pdf2image with Poppler to convert PDF pages to images for OCR processing.
Download Extracted Text: Download the extracted text as a .txt file.
Logging: Detailed logging for debugging and monitoring.

Installation and Setup
Clone the repository:

bash
Copy code
git clone <repository_url>
cd <repository_folder>
Create and activate a virtual environment:

bash
Copy code
python3.10 -m venv ocr
ocr\Scripts\activate
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Download and set up Poppler:

Download the Poppler package and extract it.
Update the POPPLER_PATH variable in the script with the path to the bin folder of Poppler.
Run the application:

bash
Copy code
python app.py
Access the application in your browser at http://localhost:5000.

Usage
Navigate to the home page.
Upload a PDF file using the provided form.
Click "Extract Text" to process the file.
View the extracted text on the screen or download it as a .txt file.

Project Structure
bash
Copy code
paddle_ocr/
├── app.py                 # Main application script
├── templates/
│   └── index.html         # HTML template for the web interface
├── uploads/               # Directory to store uploaded PDFs and results
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

Requirements
Python 3.10
PaddleOCR
pdf2image
Poppler (for PDF to image conversion)

Troubleshooting
Poppler Not Found: Ensure the POPPLER_PATH variable is correctly set to the bin directory of your Poppler installation.
PaddleOCR Errors: Check if PaddleOCR is properly installed and configured for your environment.
File Upload Issues: Verify that the uploads folder exists and has the correct permissions.