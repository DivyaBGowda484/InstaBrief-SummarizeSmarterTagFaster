# Instabrief: Summarize Smarter, Tag Faster

## Overview

**Instabrief** is an AI-powered tool that automates document summarization and tagging. It leverages Natural Language Processing (NLP) and Machine Learning (ML) techniques to generate concise summaries and contextually relevant tags for documents, making it easier for users to understand and organize large volumes of text data.

This system can be applied across various industries such as research publications, legal documents, corporate reports, and more.

## Features

* **AI-Powered Summarization**: Automatically generates concise summaries of lengthy documents by extracting key insights and core content. Includes chart-based structuring wherever it enhances document comprehension (e.g., for statistical summaries, comparisons, or structured data).
* **Contextual Tagging**: Assigns relevant keywords, named entities, and categories using contextual understanding.
* **Multilingual Support**: Supports summarization and tagging in multiple languages including English, Spanish, French, German, Kannada and more.
* **Customizable Models**: Allows training or fine-tuning models for domain-specific use cases like legal, academic, or financial documents.
* **Searchable Document Index**: Enables keyword and tag-based search using a scalable document indexing engine.
* **System Integration**: Can be integrated with external document management systems (e.g., Google Drive, Microsoft Office 365, etc.).
* **Optional Text-to-Speech Output**: Offers users the option to convert generated summaries to speech, available only for the final output.

## Tools & Technologies

- **Python**: Core programming language for backend logic.
- **FastAPI**: High-performance framework for building the backend API.
- **React + Tailwind CSS**: Modern frontend stack for a responsive and interactive UI.
- **spaCy**: For NLP tasks like tokenization, named entity recognition (NER), and part-of-speech tagging.
- **Hugging Face Transformers**: For using pre-trained transformer models like BERT, T5, and BART to perform summarization and embeddings.
- **NLTK**: For text preprocessing tasks such as stopword removal and stemming.
- **Sentence-Transformers**: Used for semantic embeddings to enable context-aware document and tag matching.
- **gTTS**: Text-to-speech library used optionally to convert output summaries into speech.
- **MongoDB**: A NoSQL document database used to store structured data like uploaded document metadata, user info, summaries, and tags.
- **Elasticsearch**: Used to enable fast, scalable, full-text search and semantic search capabilities.
- **Docker**: To containerize the backend, frontend, and database services for consistent development and deployment environments.

## Project Structure

```bash
Instabrief/
├── app/
│   ├── __init__.py             # App initialization
│   ├── summarizer.py           # Summarization logic
│   ├── extractive_summarizer.py # Extractive summarization logic
│   ├── abstractive_summarizer.py # Abstractive summarization logic
│   ├── tagger.py               # Tagging logic (keywords, entities, categories)
│   ├── search.py               # Elasticsearch integration
│   ├── db_mongo.py             # MongoDB logic (insert, retrieve, update documents)
│   ├── speech.py               # Text-to-speech module
│   └── integration.py          # External system integration
├── data/
│   ├── raw/                    # Original uploaded documents
│   ├── processed/              # Preprocessed/cleaned text data
│   └── metadata/               # Generated tags and document meta info
├── models/
│   ├── summarization_model.py  # Summarization model
│   ├── tagging_model.py        # Tagging/NER model
│   └── multilingual_models/    # Support for non-English models
├── scripts/
│   ├── train_model.py          # Model training script
│   ├── evaluate_model.py       # Model evaluation
│   └── preprocess_data.py      # Data preprocessing
├── frontend/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── pages/              # UI pages
│   │   └── App.jsx             # Main React app
│   └── tailwind.config.js      # Tailwind CSS config
├── config/
│   └── config.yaml             # App and model configurations
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker container definition
└── README.md                   # Project documentation
```

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/Instabrief-AI-Document-Summarization-Tagging.git
    cd Instabrief-AI-Document-Summarization-Tagging
    ```

2. Create and activate a virtual environment:

    - On macOS/Linux:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

    - On Windows:
      ```bash
      python -m venv venv
      venv\Scripts\activate
      ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:

    # Start FastAPI backend
    ```bash
    uvicorn app.main:app --reload
    ```

    # Start React frontend
    ```bash
      cd frontend
      npm install
      npm run dev
    ```


## Usage

- **Upload a Document**: Upload PDF, DOCX, or TXT files through the React web interface.
- **Summarization**: Extract key insights using transformer-based models; includes charts when relevant.
- **Tag Extraction**: Extract context-aware keywords, entities, and topic categories.
- **Storage**: Summaries, tags, and document metadata are stored in MongoDB.
- **Search & Retrieve**: Use Elasticsearch for high-speed keyword and semantic-based search.

## Multilingual Support

Ensure the relevant multilingual model is selected in the configuration file.  
Supported languages depend on the transformer models in use (e.g., mBART, mT5, etc.).

## Deployment

You can deploy Instabrief locally using Docker or push it to a cloud service.

### Build Docker Image

```bash
docker build -t instabrief .
```

## Run the Docker Container:

```bash
docker run -p 5000:5000 instabrief
```

This will start the app inside the container and make it available on http://localhost:5000.

## Database Setup (Local)

### MongoDB (via Docker)

```bash
docker run -d -p 27017:27017 --name instabrief-mongo mongo
```
This starts a local MongoDB instance on port 27017.

# Elasticsearch (via Docker)
```bash
docker run -d -p 9200:9200 -e "discovery.type=single-node" --name instabrief-es elasticsearch:7.17.10
```
This runs a local Elasticsearch instance accessible at http://localhost:9200.

# For the frontend:

```bash
cd frontend
npm install
npm run dev
```
This will launch the React frontend at http://localhost:3000 by default.

## Future Enhancements

- **Advanced Search**: Add semantic and question-based querying.
- **Hierarchical Tagging**: Support for nested or layered tag categories.
- **Real-Time Collaboration**: Multi-user document annotation and live editing.
- **Model Fine-Tuning Interface**: GUI to upload domain-specific data and retrain models.

## Contributing
If you'd like to contribute to the project, feel free to open an issue or submit a pull request with your improvements or bug fixes.

