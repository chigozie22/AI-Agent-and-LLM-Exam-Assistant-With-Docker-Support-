import io 
import pdfplumber
import pytesseract 
# import os
# import docx2txt
from PIL import Image
from docx import Document
import re

def extract_text_from_file(filename: str, content: bytes) -> str:
    ext = filename.lower().split(".")[-1]

    if ext == "pdf":
        return extract_text_from_pdf(content)
    
    elif ext == "docx":
        return extract_text_from_docx(content)
    elif ext in ["jpg", "jpeg", "png"]:
        return extract_text_from_image(content)
    else:
        raise ValueError("Unsupported file format")
    

def extract_text_from_pdf(content: bytes) -> str:
    text = ""
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
        return text
    
def extract_text_from_docx(content: bytes)-> str:
    doc = Document(io.BytesIO(content))
    return "\n".join([para.text] for para in doc.paragraphs)

def extract_text_from_image(content: bytes) -> str:
    image = Image.open(io.BytesIO(content))
    return pytesseract.image_to_string(image)
    
def extract_text_from_image(content: bytes) -> str:
    image = Image.open(io.BytesIO(content))
    return pytesseract.image_to_string(image)