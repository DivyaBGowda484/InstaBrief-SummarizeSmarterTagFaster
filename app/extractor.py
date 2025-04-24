# Text Extraction
# This module extracts text from various file formats including PDF, DOCX, and TXT.
# It uses PyMuPDF for PDF files and python-docx for DOCX files.
# The extracted text is returned as a string.

# Import necessary libraries
try:
    import fitz  # PyMuPDF
except ImportError:
    raise ImportError("PyMuPDF is not installed. Install it using 'pip install pymupdf'")
import docx

def extract_text(file_path):
    if file_path.endswith(".pdf"):
        doc = fitz.open(file_path)
        return " ".join([page.get_text() for page in doc])
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    elif file_path.endswith(".txt"):
        with open(file_path, 'r') as f:
            return f.read()
