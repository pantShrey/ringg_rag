from pydantic import BaseModel, Field
from typing import List, Union

# Define response models for better Swagger documentation
class UploadResponse(BaseModel):
    message: str = Field(..., description="Status message for the upload operation")

class ErrorResponse(BaseModel):
    error: str = Field(..., description="Error message describing what went wrong")

class QueryResultItem(BaseModel):
    text: str = Field(..., description="Retrieved text chunk from the document")
    chunk_id: int = Field(..., description="Identifier for the specific chunk within the document")
    similarity_score: float = Field(..., description="Similarity score between the query and the chunk (0-1 where 1 is most similar)")
    document_name: str = Field(..., description="Name of the document containing this chunk")
    vector_id: str = Field(..., description="Unique identifier for the vector in the database")

class QueryResponse(BaseModel):
    query: str = Field(..., description="Original query that was submitted")
    results: List[QueryResultItem] = Field(..., description="List of text chunks relevant to the query")

class AggregationResponse(BaseModel):
    document: str = Field(..., description="Name of the JSON document")
    field: str = Field(..., description="Field that was aggregated")
    operation: str = Field(..., description="Aggregation operation performed (max, min, sum, avg)")
    result: Union[float, int] = Field(..., description="Result of the aggregation operation")