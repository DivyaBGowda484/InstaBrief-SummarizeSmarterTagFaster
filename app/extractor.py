# Text Extraction
# This module extracts text from various file formats including PDF, DOCX, and TXT.
# It uses PyMuPDF for PDF files and python-docx for DOCX files.
# The extracted text is returned as a string.

# Import necessary libraries
import fitz  # PyMuPDF
import docx
import os

def extract_text(file_path):
    try:
        if file_path.endswith(".pdf"):
            with fitz.open(file_path) as doc:
                return " ".join([page.get_text() for page in doc])
        elif file_path.endswith(".docx"):
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        elif file_path.endswith(".txt"):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file type: {file_path}")
    except Exception as e:
        print(f"Error extracting text from file {file_path}: {e}")
        return None
    
    