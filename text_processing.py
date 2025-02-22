import json
import pymupdf  # PyMuPDF
import docx
import tiktoken
import re

# Helper Function: Extract text from files
def extract_text(file_path, file_type):
    """
    Extract text content from various file formats.
    
    Args:
        file_path: Path to the file
        file_type: Type of file ('pdf', 'docx', 'json', 'txt')
        
    Returns:
        str: Extracted text content
    """
    text = ""
    if file_type == "pdf":
        doc = pymupdf.open(file_path)
        for page in doc:
            text += page.get_text("text") + "\n"
    elif file_type == "docx":
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text + "\n"
    elif file_type == "json":
        with open(file_path, "r", encoding="utf-8") as f:
            json_data = json.load(f)
            text = json.dumps(json_data, indent=2)  # Convert JSON to string
    elif file_type == "txt":
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    return text

# Helper Function: Chunk text
def chunk_text(text, filetype, chunk_size=300, overlap=50):
    """
    Chunks text into overlapping segments while preserving sentence boundaries.
    
    Args:
        text: Text to chunk
        filetype: Type of file ('pdf', 'docx', 'json', 'txt')
        chunk_size: Maximum token size for each chunk
        overlap: Number of tokens to overlap between chunks
        
    Returns:
        list: List of text chunks
    """
    if filetype == "json":
        try:
            objects = json.loads(text)  # Parse JSON
            chunks = [json.dumps(obj, ensure_ascii=False) for obj in objects]  # Chunk by objects
            return chunks
        except json.JSONDecodeError:
            print("Error: Invalid JSON format")
            return []
    
    # Tokenize text
    encoding = tiktoken.get_encoding("cl100k_base")  # OpenAI's tokenizer
    tokens = encoding.encode(text)  # Convert text to tokens
    
    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + chunk_size, len(tokens))  # Define chunk range
        
        # Convert tokens back to text
        chunk_text = encoding.decode(tokens[start:end])
        
        # Adjust chunk to respect sentence boundaries
        if end < len(tokens):  # Avoid adjusting on last chunk
            match = re.search(r'(?<=\.)\s+[A-Z]', chunk_text[::-1])  # Look for a period followed by a capital letter
            if match:
                end -= match.start()  # Adjust endpoint to align with sentence

        # Add chunk to list
        chunks.append(encoding.decode(tokens[start:end]))
        
        # Move start position with overlap
        start += chunk_size - overlap  

    return chunks