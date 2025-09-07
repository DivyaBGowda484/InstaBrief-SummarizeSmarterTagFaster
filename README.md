# Instabrief: Summarize Smarter, Tag Faster

## Overview

**Instabrief** is a full-stack AI-powered tool that automates document summarization and tagging. It leverages **Natural Language Processing (NLP)** and **Machine Learning (ML)** techniques to generate concise summaries and contextually relevant tags for documents, making it easier for users to understand and organize large volumes of text data.

This system can be applied across various industries such as research publications, legal documents, corporate reports, healthcare, and more.

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

## Installation, Usage, and Contribution

### Installation

**Option 1: Using Docker (Recommended)**  
1. Make sure Docker Desktop is installed.  
2. Build and start services:  
   ```bash
   docker compose up -d --build
    ```

## Installation, Usage, and Contribution

### Open Services
- **API**: [http://localhost:8000/health](http://localhost:8000/health)  
- **Frontend**: [http://localhost:5173](http://localhost:5173)  

### Option 2: Local Development (without Docker)

**Backend (FastAPI)**  
```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Local Development, Usage, and Contribution

### Frontend (React + Tailwind)
```bash
cd frontend
npm install
npm run dev
```

## Databases, Usage, and Contribution

### Databases (via Docker)
- **MongoDB**  
  ```bash
  docker run -d -p 27017:27017 --name instabrief-mongo mongo
    ```

### Elasticsearch
```bash
docker run -d -p 9200:9200 -e "discovery.type=single-node" --name instabrief-es elasticsearch:7.17.10
```

## Usage
- **Upload a Document**: Upload PDF, DOCX, or TXT files through the React web interface.  
- **Summarization**: Extract key insights using transformer-based models; includes charts when relevant.  
- **Tag Extraction**: Extract context-aware keywords, entities, and topic categories.  
- **Storage**: Summaries, tags, and document metadata are stored in MongoDB.  
- **Search & Retrieve**: Use Elasticsearch for high-speed keyword and semantic-based search.  

## Notes
- First summarization loads `facebook/bart-large-cnn`.  
- spaCy model `en_core_web_sm` downloads on first NLP call.  
- MongoDB runs at `mongodb://localhost:27017`.  
- Elasticsearch runs at `http://localhost:9200`.  

## Tests
```bash
pytest -q
```

## Future Enhancements
- **Advanced Search**: Add semantic and question-based querying.  
- **Hierarchical Tagging**: Support for nested or layered tag categories.  
- **Real-Time Collaboration**: Multi-user document annotation and live editing.  
- **Model Fine-Tuning Interface**: GUI to upload domain-specific data and retrain models.  

## Contributing
If you'd like to contribute to the project, feel free to open an issue or submit a pull request with your improvements or bug fixes.  
