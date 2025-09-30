import os
from fastapi import APIRouter, File, UploadFile, status
from fastapi.responses import JSONResponse
from weaviate.classes.query import Filter
import database
from text_processing import extract_text, chunk_text
from models import UploadResponse, ErrorResponse

router = APIRouter(tags=["Document Management"])

@router.post(
    "/upload", 
    response_model=UploadResponse,
    responses={
        200: {"description": "Document successfully uploaded and processed"},
        400: {"model": ErrorResponse, "description": "Bad request, such as unsupported file format"},
        500: {"model": ErrorResponse, "description": "Server error during processing"}
    },
    summary="Upload and process a document",
    description="""
    Upload a document file (PDF, DOCX, JSON, or TXT) to be processed and indexed.
    
    The system will:
    1. Extract text from the document
    2. Split the text into meaningful chunks
    3. Generate embeddings for each chunk
    4. Store the chunks and embeddings in the vector database
    
    If a document with the same name already exists, it will be replaced.
    """
)
async def upload_document(file: UploadFile = File(..., description="The document file to upload and process")):
    try:
        # Check file extension
        file_extension = file.filename.split(".")[-1].lower()
        if file_extension not in ["pdf", "docx", "json", "txt"]:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": f"Unsupported file format: {file_extension}. Supported formats are PDF, DOCX, JSON, and TXT"}
            )
            
        file_path = f"temp_{file.filename}"
        # Get Weaviate client
        client = database.get_client()
        collection = client.collections.get("Documents")

        
        try:
            existing_objects = collection.query.fetch_objects(
                filters=Filter.by_property("filename").equal(file.filename),
                limit=1
            )
            
            if existing_objects.objects:
                return JSONResponse(
                    status_code=status.HTTP_409_CONFLICT,
                    content={"error": "Upload failed: file name already exists"}
                )
        except Exception as e:
            print(f"Warning: Could not check for existing files: {str(e)}")
        # Save file temporarily
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Extract text
        file_type = file.filename.split(".")[-1].lower()
        text = extract_text(file_path, file_type)
        chunks = chunk_text(text, file_type)



        # Store new embeddings
        with collection.batch.dynamic() as batch:
            for i, chunk in enumerate(chunks):
                batch.add_object(
                    properties={"filename": file.filename, "text_chunk": chunk, "chunk_id": i}
                )

        os.remove(file_path)
        return {"message": f"{file.filename} uploaded and processed successfully. {len(chunks)} chunks were created and indexed."}
        
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Upload failed: {str(e)}"}
        )