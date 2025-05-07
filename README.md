🧠 AI Agent & LLM Exam Assistant (with Docker Support)
This project is a full-stack AI-powered assistant designed to help students extract insights from lecture notes and past exam questions. It uses Large Language Models (LLMs), document parsing, OCR, and a multimodal interface to summarize content, answer questions, and even generate likely exam questions.

🚀 Fully containerized with Docker and deployable with Docker Compose.

✅ Problem Statement
Many students struggle to:

Understand dense lecture notes quickly.

Prepare efficiently for exams using past questions.

Access an integrated tool that can read, understand, and interact with academic material (PDFs, DOCX, images).

This project solves these problems by:

Using LLMs to summarize lecture content.

Analyzing past exam questions to generate likely future questions.

Providing an AI agent interface to answer student queries contextually.

Using OCR to handle handwritten or image-based documents.

🧰 Tech Stack
🖥️ Frontend
Streamlit – for an interactive web interface

🧠 Backend
FastAPI – for serving AI endpoints

LangChain – to manage LLM tool usage and agent workflows

Sentence-Transformers – for extractive summarization and question matching

Transformers (HuggingFace) – for handling text models

PyMuPDF, pdfplumber, python-docx – to extract content from PDFs and DOCX

Tesseract OCR + OpenCV – to process image documents

🧱 Infrastructure
Docker – containerization of backend, frontend, and AI models

Docker Compose – for orchestrating multi-service setup with GPU support

NVIDIA Docker – to enable CUDA GPU acceleration in containers

🧪 Features
🔍 Extract lecture notes from PDFs, DOCX, and images.

📝 Summarize key points from large content using LLMs.

🎯 Generate likely future exam questions based on past formats.

💬 Answer student questions contextually using the uploaded notes.

🧠 Uses TinyLlama and other models offline for resource-efficient performance.

🐳 Fully Dockerized with GPU acceleration (CUDA 12.6 supported).
