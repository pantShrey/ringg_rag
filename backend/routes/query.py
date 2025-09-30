import json
from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from weaviate.classes.query import MetadataQuery, Filter
import database
from models import QueryResponse, ErrorResponse, AggregationResponse

router = APIRouter()

@router.get(
    "/query", 
    response_model=QueryResponse,
    tags=["Document Retrieval"],
    responses={
        200: {"description": "Query successfully executed"},
        404: {"model": ErrorResponse, "description": "Document not found"},
        500: {"model": ErrorResponse, "description": "Server error during query"}
    },
    summary="Query a document using semantic search",
    description="""
    Retrieve the most relevant text chunks from a specific document based on a natural language query.
    
    The system will:
    1. Convert your query to an embedding vector
    2. Find the most semantically similar chunks in the specified document
    3. Return the text chunks along with relevance scores and metadata
    
    Results are ordered by similarity to your query.
    """
)
async def query_document(
    document_name: str = Query(..., description="Name of the document to query"), 
    query: str = Query(..., description="Natural language query to search for in the document"),
    top_k: int = Query(3, description="Number of results to return", ge=1, le=20)
):
    try:
        client = database.get_client()
        collection = client.collections.get("Documents")
        
        # Check if document exists
        doc_check = collection.query.fetch_objects(
            filters=Filter.by_property("filename").equal(document_name),
            limit=1
        )
        
        if len(doc_check.objects) == 0:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={"error": f"Document '{document_name}' not found"}
            )
        
        response = collection.query.near_text(
            query=query,
            filters=Filter.by_property("filename").equal(document_name),
            limit=top_k,
            return_metadata=MetadataQuery(distance=True)
        )
        
        # Enhanced metadata in results
        results = [
            {
                "text": obj.properties["text_chunk"],
                "chunk_id": obj.properties["chunk_id"],
                "similarity_score": 1 - obj.metadata.distance,  # Convert distance to similarity
                "document_name": document_name,
                "vector_id": str(obj.uuid)  # Convert UUID to string
            }
            for obj in response.objects
        ]
        
        return {"query": query, "results": results}
        
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Query failed: {str(e)}"}
        )

@router.get(
    "/json-query", 
    response_model=AggregationResponse,
    responses={
        200: {"description": "Aggregation successfully executed"},
        400: {"model": ErrorResponse, "description": "Invalid operation or parameter"},
        404: {"model": ErrorResponse, "description": "Document or field not found"},
        500: {"model": ErrorResponse, "description": "Server error during aggregation"}
    },
    tags=["JSON Operations"],
    summary="Perform aggregation operations on JSON documents",
    description="""
    Run aggregation operations on numerical fields in JSON documents.
    
    Supported operations:
    - max: Find the maximum value of the specified field
    - min: Find the minimum value of the specified field
    - sum: Calculate the sum of all values for the specified field
    - avg: Calculate the average (mean) of all values for the specified field
    
    This endpoint is useful for quick data analysis.
    """
)
async def json_query(
    document_name: str = Query(..., description="Name of the JSON document to analyze"),
    field: str = Query(..., description="Field name to aggregate "),
    operation: str = Query(..., description="Aggregation operation (max, min, sum, avg)")
):
    try:
        if operation not in ["max", "min", "sum", "avg"]:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Invalid operation. Supported operations are: max, min, sum, avg"}
            )
            
        client = database.get_client()
        collection = client.collections.get("Documents")

        # Check if document exists and is JSON
        doc_check = collection.query.fetch_objects(
            filters=Filter.by_property("filename").equal(document_name),
            limit=1
        )
        
        if len(doc_check.objects) == 0:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND, 
                content={"error": f"Document '{document_name}' not found"}
            )
            
        if not document_name.lower().endswith('.json'):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "This operation is only supported for JSON documents"}
            )

        # Fetch all objects (chunks) belonging to the given document
        response = collection.query.fetch_objects(
            filters=Filter.by_property("filename").equal(document_name)
        )

        # Merge JSON chunks into a single list
        json_chunks = [json.loads(obj.properties["text_chunk"]) for obj in response.objects]

        # Extract values for the given field
        values = [entry[field] for entry in json_chunks if field in entry]

        if not values:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"error": f"Field '{field}' not found in document '{document_name}'"}
            )
            
        # Check if values are numeric
        if not all(isinstance(val, (int, float)) for val in values):
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": f"Field '{field}' contains non-numeric values. Aggregation requires numeric data."}
            )

        # Perform requested aggregation
        if operation == "max":
            result = max(values)
        elif operation == "min":
            result = min(values)
        elif operation == "sum":
            result = sum(values)
        elif operation == "avg":
            result = sum(values) / len(values)

        return {"document": document_name, "field": field, "operation": operation, "result": result}
        
    except json.JSONDecodeError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": "Invalid JSON format in document chunks"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Operation failed: {str(e)}"}
        )