### 🚀 Node.js Interview Prep – RAG Application

- A Retrieval-Augmented Generation (RAG) based application designed to help developers prepare for Node.js interviews by asking natural language questions and receiving context-aware, accurate answers sourced from curated documents.

- This project uses Flask to expose APIs, a vector database for semantic search, and LLM-powered generation to deliver concise and relevant interview explanations.


### ✨ Features

- 📄 Upload Node.js interview PDFs / documents

- 🔍 Semantic search using vector embeddings

- 🧠 RAG pipeline for accurate, context-aware answers

- ⚡ Flask-based REST APIs

- 🔐 API key–protected endpoints

- 🚦 Rate limiting to prevent abuse

- 🗃 Persistent vector storage

- 🧩 Modular & extensible architecture


#### 🧠 How It Works (High Level)
PDF / Docs
    ↓
Document Loader
    ↓
Text Chunking
    ↓
Embedding Generation
    ↓
Vector Database
    ↓
Semantic Retrieval
    ↓
LLM Answer Generation
    ↓
Response

### 🛠️ Tech Stack

Backend: Flask (Python)

LLM / Embeddings: Sentence Transformers / LLM API (Groq)

Vector DB: ChromaDB

Auth: API Key–based protection

Server: Waitress (Windows-compatible)

### 🚀 Future Improvements

UI frontend (React)

Background PDF ingestion

Per-user collections

Streaming responses

Multi-language interview support

Dockerized deployment

### 📌 Why This Project?

This project was built to:

Deepen understanding of RAG systems

Apply GenAI in real-world developer workflows

Build a production-ready backend with security & scalability in mind

Create a practical tool for interview preparation

### 👤 Author

Saurabh Manohar
Full Stack / Backend Engineer
Focused on scalable systems, APIs, and GenAI integrations