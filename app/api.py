# Importing custom modules for text extraction, preprocessing, summarization, and tagging
from app.extractor import extract_text  # Extracts text from uploaded files
from scripts.preprocess_data import clean_text  # Cleans and preprocesses the extracted text
from app.summarizer import generate_summary  # Generates a summary of the cleaned text
from app.tagger import extract_keywords, extract_entities, classify_document  # Extracts keywords, entities, and classifies text

# Importing FastAPI and other necessary libraries
from fastapi import FastAPI, UploadFile, File  # FastAPI for creating the API, UploadFile for handling file uploads
import shutil  # For file operations like copying

# Initialize the FastAPI application
app = FastAPI()

@app.post("/process/")
async def process_file(file: UploadFile = File(...)):
    """
    Endpoint to process an uploaded file. It extracts text, cleans it, generates a summary,
    extracts keywords and entities, and classifies the document into a category.

    Parameters:
        file (UploadFile): The uploaded file to process.

    Returns:
        dict: A dictionary containing the summary, keywords, entities, and category of the document.
    """
    # Define the temporary file path where the uploaded file will be saved
    temp_path = f"temp_files/{file.filename}"

    # Save the uploaded file to the temporary directory
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract raw text from the uploaded file
    raw_text = extract_text(temp_path)

    # Clean and preprocess the extracted text
    cleaned_text = clean_text(raw_text)

    # Generate a summary of the cleaned text
    summary = generate_summary(cleaned_text)

    # Extract keywords from the cleaned text
    keywords = extract_keywords(cleaned_text)

    # Extract named entities from the cleaned text
    entities = extract_entities(cleaned_text)

    # Classify the document into one of the predefined categories
    category = classify_document(summary, ["Legal", "Medical", "Finance", "Research"])

    # Return the processed results as a JSON response
    return {
        "summary": summary,  # The generated summary
        "keywords": keywords,  # The extracted keywords
        "entities": entities,  # The extracted named entities
        "category": category  # The classified category
    }