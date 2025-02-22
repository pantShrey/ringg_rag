from fastapi import FastAPI
from routes import documents, query, system
import database

# FastAPI App with metadata for Swagger UI
app = FastAPI(
    title="Document Retrieval API",
    description="""
    A Retrieval Augmented Generation (RAG) system that ingests documents,
    generates embeddings, and allows semantic search within document content.
    
    This API supports document upload and semantic search in PDF, DOCX, JSON, and TXT formats.
    """,
    version="1.0.0",
    contact={
        "name": "Shrey Pant",
        "email": "pantshrey01@gmail.com",
    },
)

# Include routers
app.include_router(documents.router)
app.include_router(query.router)
app.include_router(system.router)

# Shutdown Hook: Close Weaviate connection
@app.on_event("shutdown")
def shutdown():
    database.close_client()