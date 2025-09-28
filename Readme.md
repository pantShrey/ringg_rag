# RAG System with Weaviate

A Retrieval Augmented Generation (RAG) system that uses Weaviate as its vector database for semantic document search and retrieval.

## Overview

This system enables you to upload documents in various formats (PDF, DOCX, JSON, TXT), automatically processes them into embeddings, and allows for semantic search across document content. The system features a modular architecture, automated document monitoring, and efficient retrieval capabilities.

## Features

- **Document Ingestion Pipeline**: Uploads and processes PDF, DOCX, JSON, and TXT files
- **Embedding Generation**: Creates vector embeddings using Cohere's embedding models
- **Semantic Search**: Retrieves relevant document sections based on natural language queries
- **Automated Document Processing**: Monitors a directory for new documents and automatically processes them
- **JSON Aggregation**: Performs aggregation operations on JSON documents (max, min, sum, avg)
- **Modular Architecture**: Clean separation of concerns for maintainability and extensibility

## System Architecture

The system is built with a modular architecture consisting of:

```
config.py               # Configuration settings and constants
main.py                 # Application entry point
text_processing.py      # Text extraction and chunking logic
database.py             # Weaviate database connection and operations
models.py               # Pydantic models for request/response validation
watcher_service.py      # Document monitoring service
documents/              # Directory for document storage and monitoring
routes/                 # API route definitions
└── __init__.py
└── documents.py        # Document upload and management endpoints
└── query.py            # Query and retrieval endpoints
└── system.py           # System health and status endpoints
```

### Workflow

1. **Document Upload**: Documents are uploaded via API or placed in the monitored directory
2. **Text Extraction**: Text is extracted from various document formats
3. **Text Chunking**: Documents are split into semantic chunks with context preservation
4. **Embedding Generation**: Vector embeddings are created for each chunk using Cohere
5. **Storage**: Chunks and embeddings are stored in Weaviate
6. **Query Processing**: Natural language queries are converted to embeddings and matched against stored document chunks
7. **Retrieval**: The most relevant document chunks are returned based on semantic similarity

## API Documentation

### Upload Endpoint

```
POST /upload
```

Uploads a document and processes it for retrieval.

**Request**:
- Form data with key `file` containing the document to upload
- Supported formats: PDF, DOCX, JSON, TXT

**Response**:
```json
{
  "message": "document.pdf uploaded and processed successfully. 15 chunks were created and indexed."
}
```

### Query Endpoint

```
GET /query
```

Retrieves relevant text chunks from a document based on a query.

**Parameters**:
- `document_name` (string, required): Name of the document to query
- `query` (string, required): Natural language query
- `top_k` (integer, optional, default=3): Number of results to return

**Response**:
```json
{
  "query": "What are the key metrics?",
  "results": [
    {
      "text": "The key performance metrics include customer acquisition cost (CAC), lifetime value (LTV), monthly recurring revenue (MRR), and churn rate.",
      "chunk_id": 5,
      "similarity_score": 0.87,
      "document_name": "metrics.pdf",
      "vector_id": "uuid-string"
    },
    ...
  ]
}
```

### JSON Aggregation Endpoint

```
GET /json-query
```

Performs aggregation operations on JSON documents.

**Parameters**:
- `document_name` (string, required): Name of the JSON document
- `field` (string, required): Field to perform operations on
- `operation` (string, required): One of "max", "min", "sum", "avg"

**Response**:
```json
{
  "document": "data.json",
  "field": "price",
  "operation": "avg",
  "result": 45.67
}
```

### Health Check Endpoint

```
GET /health
```

Verifies system health and connectivity.

**Response**:
```json
{
  "status": "healthy",
  "weaviate_connection": "ok"
}
```

## Installation and Setup

### Prerequisites

- Python 3.9+
- [Weaviate Cloud Account](https://weaviate.io/console/dashboard) or self-hosted Weaviate instance
- [Cohere API key](https://dashboard.cohere.com/api-keys)

### Local Setup

1. Fork & Clone this repository
   ```bash
   git clone https://github.com/yourusername/ringg_rag.git
   cd ringg_rag
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your API keys
   ```
   WEAVIATE_URL=your-weaviate-cluster-url
   WEAVIATE_API_KEY=your-weaviate-api-key
   COHERE_API_KEY=your-cohere-api-key
   WATCH_DIRECTORY=./documents
   ```

5. Run the application
   ```bash
   uvicorn main:app --reload
   ```

6. In a separate terminal, run the document watcher (optional)
   ```bash
   python watcher_service.py
   ```

### Docker Deployment

1. Build and run with Docker Compose
   ```bash
   docker-compose up -d
   ```

## Design Choices and Trade-offs

### Vector Database Selection

We chose Weaviate as our vector database because it offers:
- Strong performance for semantic search operations
- Built-in support for multiple embedding models
- Good documentation and community support
- Ability to filter and combine metadata queries with vector search

Trade-off: Weaviate has higher resource requirements compared to simpler vector stores, but provides better querying capabilities.

### Chunking Strategy

Our text chunking strategy focuses on preserving semantic boundaries by:
- Respecting sentence and paragraph boundaries
- Using token-based chunking with overlap for context preservation
- Special handling for structured data like JSON

Trade-off: More sophisticated chunking adds processing overhead but improves retrieval quality significantly.

### Document Monitoring

The document watcher service provides automated document processing with:
- Real-time monitoring for new files
- Automatic processing and embedding generation
- Cleanup after successful processing

Trade-off: The file system-based approach is simple but has scalability limitations for high-volume scenarios.

## Future Improvements

### Redis Caching Layer

While Weaviate has internal caching, adding an explicit Redis caching layer would:
- Reduce redundant embedding calculations for frequent queries
- Improve response times for common queries
- Decrease API costs for embedding models

### Cloud Storage Integration

Replacing local document storage with S3:
- AWS Lambda functions could trigger processing when new documents are uploaded to S3
- Eliminates need to store documents on the application server
- Provides better scalability and durability

### Message Queue Integration

Adding SQS or RabbitMQ for document processing:
- Enables asynchronous processing for better scalability
- Provides retry capabilities for failed processing
- Allows better load balancing across multiple processor instances

### Observability Enhancement

Integration with LangSmith or a custom SQL-based tracking system would provide:
- Better visibility into query performance
- Tracking of usage patterns
- Identification of query patterns for optimization
- A/B testing of different embedding models or chunking strategies

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
