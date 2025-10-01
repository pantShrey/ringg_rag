# Retrieval-Augmented Generation (RAG) Document Assistant

A full-stack, containerized RAG system with a **Next.js/Tailwind CSS frontend** and a **FastAPI/Weaviate backend**. This application allows you to upload documents (PDF, DOCX, JSON, TXT), perform semantic search with AI, and extract numerical insights via JSON analytics—all orchestrated locally with Docker Compose.

## Live Demo
[Try it out here!](https://ringg-rag-six.vercel.app/)

### Testing Samples

- **test_document.txt**
Solar System description; query: “What is the Great Red Spot?”
- **data.json**

```json
[
  {"region":"North","sales":1500,"expenses":800,"profit":700},
  {"region":"South","sales":1200,"expenses":600,"profit":600},
  {"region":"East","sales":1700,"expenses":900,"profit":800}
]
```

Analytics examples:
    - Max `sales` → `1700`
    - Avg `profit` → `700`
    - Sum `expenses` → `2300`



## Key Features

-   **Modern Frontend**: A clean, responsive user interface built with Next.js, TypeScript, and Tailwind CSS.
-   **Interactive Document Upload**: Easy drag-and-drop or file browser uploads directly from the UI.
-   **Semantic Search Interface**: Query uploaded documents using natural language and view similarity-ranked results.
-   **JSON Analytics Dashboard**: Compute aggregations (max, min, sum, avg) on numeric fields within uploaded JSON documents.
-   **Backend Document Pipeline**: Ingests and processes PDF, DOCX, JSON, and TXT files, creating vector embeddings for semantic search.
-   **Automated Document Processing**: A background `watcher` service monitors a directory for new documents and processes them automatically.
-   **Fully Containerized**: The entire stack—FastAPI backend, Next.js frontend, and document watcher—is managed by Docker Compose for easy setup and deployment.

## System Architecture

The project is divided into a `frontend` application and a `backend` API, orchestrated by Docker.

### Repository Structure

```
/ringg_rag
│
├── backend/                     # FastAPI application
│   ├── main.py                  # App entry, CORS, routers
│   ├── routes/                  # API endpoints (documents, query, system)
│   ├── database.py              # Weaviate client connector
│   ├── text_processing.py       # Text extraction and chunking logic
│   ├── models.py                # Pydantic data schemas
│   └── requirements.txt         # Python dependencies
│
├── frontend/                    # Next.js (App Router) application
│   ├── app/
│   │   ├── layout.tsx           # Root layout & ToastProvider
│   │   ├── page.tsx             # Main page with navigation logic
│   │   ├── components/          # Reusable UI components (Navbar, pages, ui/)
│   │   └── globals.css          # Tailwind CSS theme variables
│   ├── package.json             # Frontend dependencies
│   ├── tsconfig.json            # TypeScript configuration
│   └── ...
│
├── documents/                   # Monitored directory for file uploads
│
├── .env                         # Environment variables (API keys, URLs)
├── docker-compose.yml           # Service orchestration (backend, frontend, watcher)
├── Dockerfile                   # Dockerfile for the backend service
└── Dockerfile.frontend          # Dockerfile for the frontend service
```

### Workflow

1.  **Document Upload**: A user uploads a file via the frontend UI, or a file is placed in the `documents/` directory.
2.  **Processing**: The FastAPI API or `watcher_service` receives the file.
3.  **Text Extraction & Chunking**: Text is extracted and split into semantic chunks.
4.  **Embedding Generation**: Vector embeddings are created for each chunk (e.g., using Cohere).
5.  **Storage**: The text chunks and their corresponding embeddings are stored in the Weaviate vector database.
6.  **Query**: A user submits a natural language query through the frontend.
7.  **Retrieval**: The query is converted into an embedding, and Weaviate performs a similarity search to find the most relevant document chunks.
8.  **Response**: The results are returned to the frontend and displayed to the user.

## Getting Started

### Prerequisites

-   Docker & Docker Compose
-   Weaviate Cloud Account or a self-hosted instance
-   Cohere API key (or another embedding provider)

### Setup & Run with Docker Compose

This is the recommended way to run the application.

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/pantshrey/ringg_rag.git
    cd ringg_rag
    ```

2.  **Create Environment File**
    Create a `.env` file in the project root. Copy the contents of `.env.example` (if provided) or add the following variables:
    ```
    WEAVIATE_URL=your-weaviate-cluster-url
    WEAVIATE_API_KEY=your-weaviate-api-key
    COHERE_API_KEY=your-cohere-api-key
    ```

3.  **Build and Start All Services**
    ```bash
    docker-compose up --build
    ```
    To run in the background (detached mode), use `docker-compose up -d --build`.

4.  **Access the Application**
    -   **Frontend UI**: [http://localhost:3000](http://localhost:3000)
    -   **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
    -   **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

5.  **Stopping the Application**
    ```bash
    docker-compose down
    ```

## Usage Guide

### 1. Upload a Document

-   Navigate to the **Upload** tab in the UI.
-   Click the upload area to browse for a file or drag and drop a PDF, DOCX, JSON, or TXT file.
-   Click the **Upload File** button. A progress bar will show the upload status.

### 2. Query a Document

-   Navigate to the **Query** tab.
-   Enter the exact **Document Name** (e.g., `report.pdf`) you uploaded.
-   Type your question in the **Query** text area (e.g., “What were the quarterly earnings?”).
-   Adjust the **Number of Results** slider if needed.
-   Click **Search**. The most relevant text chunks will appear, ranked by similarity score.

### 3. Aggregate/Analyse a JSON Document

-   Navigate to the **Analytics** tab.
-   Enter the **Document Name** of an uploaded JSON file (e.g., `sales_data.json`).
-   Enter the **Field** you want to analyze (must contain numeric data, e.g., `sales`).
-   Select an **Operation** (Maximum, Minimum, Sum, or Average).
-   Click **Calculate** to see the result.

---

## API Documentation

For direct interaction with the backend, use the following endpoints.

#### `POST /upload`

Uploads and processes a document.
-   **Request**: `multipart/form-data` with a `file` key.
-   **Response** (200 OK):
    ```json
    {
      "message": "report.pdf uploaded and processed successfully. 25 chunks were created and indexed."
    }
    ```

#### `GET /query`

Performs a semantic search on a document.
-   **Query Parameters**:
    -   `document_name` (string, required)
    -   `query` (string, required)
    -   `top_k` (integer, optional, default: 3)
-   **Response** (200 OK):
    ```json
    {
      "query": "What were the quarterly earnings?",
      "results": [
        {
          "text": "The quarterly earnings showed a 15% increase, driven by strong performance in the North American market.",
          "chunk_id": 12,
          "similarity_score": 0.91,
          "document_name": "report.pdf",
          "vector_id": "..."
        }
      ]
    }
    ```

#### `GET /json-query`

Performs an aggregation on a JSON document.
-   **Query Parameters**:
    -   `document_name` (string, required)
    -   `field` (string, required)
    -   `operation` (string, required: `max`, `min`, `sum`, `avg`)
-   **Response** (200 OK):
    ```json
    {
      "document": "sales_data.json",
      "field": "sales",
      "operation": "sum",
      "result": 5400
    }
    ```

#### `GET /health`

Checks the API and database connection status.
-   **Response** (200 OK):
    ```json
    {
      "status": "healthy",
      "weaviate_connection": "ok"
    }
    ```

## Design Choices & Future Improvements

### Technology Stack
-   **Vector Database (Weaviate)**: Chosen for its strong performance, metadata filtering, and built-in support for various embedding models.
-   **Chunking Strategy**: Our strategy respects sentence/paragraph boundaries and uses overlap to preserve semantic context, improving retrieval quality at the cost of slightly more processing overhead.
-   **Frontend (Next.js)**: Provides a modern, fast, and maintainable foundation for the user interface, with server-side rendering capabilities for future expansion.

### Future Work
-   **Redis Caching**: Implement a Redis layer to cache embedding results for common queries, reducing latency and API costs.
-   **Cloud Storage Integration**: Replace the local `documents` directory with an S3 bucket and trigger processing via Lambda functions for better scalability.
-   **Asynchronous Processing**: Integrate a message queue (e.g., SQS or RabbitMQ) to decouple the upload from the processing, making the system more resilient and scalable.
-   **Enhanced Observability**: Integrate with a tool like LangSmith to track query performance, identify patterns, and A/B test different chunking strategies or models.

## Contributing

Contributions are welcome! Please feel free to fork the repository and submit a Pull Request.

## License

This project is licensed under the MIT License.
