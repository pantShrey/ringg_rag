from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
import database

router = APIRouter(tags=["System"])

@router.get(
    "/health",
    summary="Check system health",
    description="Verify if the API and its connections to Weaviate are working properly."
)
async def health_check():
    try:
        # Test Weaviate connection
        client = database.get_client()
        collection = client.collections.get("Documents")
        return {"status": "healthy", "weaviate_connection": "ok"}
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "unhealthy", "error": str(e)}
        )