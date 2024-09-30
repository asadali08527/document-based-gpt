
# Document-based GPT Backend

This is a backend project for a document-based GPT system that allows users to upload documents, and later query these documents using natural language queries. The solution is built using a microservice architecture, and employs a vector store (FAISS) for document embeddings, allowing fast retrieval of relevant content based on user queries.

## Project Overview

The backend provides APIs to:
- Register users as either "admin" or "user". Admins have the right to upload documents to the system.
- Authenticate users and issue JWT tokens for secure access.
- Allow admins to upload text documents, which are processed and stored as vectors for efficient search.
- Allow both admins and users to ask natural language questions based on the content of uploaded documents.

The vector store is built using FAISS, and OpenAI's language models are used for generating embeddings. The solution uses FastAPI as the web framework for its simplicity, speed, and automatic API documentation features.

## Tech Stack and Libraries

The following technologies and libraries are used in this project:

- **FastAPI**: Web framework for building APIs quickly and efficiently.
- **OpenAI**: To integrate and generate embeddings for document content.
- **FAISS**: Facebook AI Similarity Search for vector storage.
- **LangChain**: To handle document processing and vector store operations.
- **JWT**: For token-based authentication and secure access.
- **Python Libraries**:
    - `passlib`: For password hashing.
    - `python-jose`: For creating and verifying JWT tokens.
    - `better-profanity`: For filtering inappropriate content from queries.
    - `uvicorn`: For running the ASGI server.
    - `pydantic`: For data validation and settings management.

## Project Directory Structure

The project is organized as follows:

```
app/
├── api/
│   └── v1/
│       └── routers/        # API routes for authentication, document upload, and querying
│       └── controllers/    # Controllers to handle the business logic for API routes
├── core/
│   └── config.py           # Application configuration settings
│   └── logging_config.py   # Logging configuration for debugging and tracking
├── db/
│   └── faiss_store.py      # Functions to handle FAISS vector store operations
├── models/
│   └── user.py             # User model for registration
│   └── token.py            # JWT token model
├── schemas/
│   └── auth.py             # Request and response schemas for authentication
│   └── query.py            # Schema for handling user queries
├── services/
│   └── auth_service.py     # Services for user registration and login
│   └── document_service.py # Service for document uploading and processing
│   └── query_service.py    # Service to handle user queries and generate answers
│   └── vector_store_service.py # Service to interact with vector store operations
├── utils/
│   └── auth_util.py        # Utility functions for authentication checks
│   └── document_util.py    # Utility functions for document processing
│   └── query_util.py       # Utility functions for query processing
│   └── security_util.py    # Utility functions for password hashing and token creation
├── main.py                 # Main application entry point
.env                        # Environment file to store sensitive keys and configurations
requirements.txt            # Python dependencies for the project
Dockerfile                  # Docker configuration file
```

## Key Classes and Methods

### 1. **VectorStoreService**
   - **create_vector_store**: Initializes the FAISS vector store by loading documents, generating embeddings, and saving them to the vector store.
   - **add_document_to_vector_store**: Adds a new document to the vector store, updates the stored vectors, and reloads the QA chain.
   - **get_relevant_documents**: Retrieves relevant documents based on a query from the vector store.

### 2. **AuthController & AuthService**
   - Handles user registration and login, password hashing, and JWT token creation.

### 3. **DocumentController & DocumentService**
   - Manages document upload, saving files to the server, and updating the vector store.

### 4. **QueryController & QueryService**
   - Processes user queries, retrieves relevant documents, and returns a response based on the content of the uploaded documents.

## How to Run the Solution

### 1. Update the .env File
Before starting the application, make sure you have the following environment variables set in the `.env` file:

```env
ADMIN_KEY=my_admin_key_here
SECRET_KEY=my_jwt_secret_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

### 2. Docker Build and Run

You can build and run the Docker container using the following commands:

```bash
docker build -t document_based_gpt_backend:latest .
docker run -p 8000:8000 --env-file .env document_based_gpt_backend:latest
```

### 3. Access the API
Once the container is running, you can access the API documentation and test the endpoints at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

You can register as an `admin` or `user` and start using the APIs. If registering as an `admin`, you will need to provide the `admin_key`.

## API Endpoints

### 1. Register User (Admin/User)
```bash
curl -X 'POST'   'http://127.0.0.1:8000/v1/auth/register/'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '{
  "username": "admin",
  "password": "testpassword",
  "role": "admin",
  "admin_key": "admin_key_here"
}'
```
**Response:**
```json
{
 "message": "User registered successfully"
}
```

### 2. Get JWT Token
```bash
curl -X 'POST'   'http://127.0.0.1:8000/v1/auth/token/'   -H 'accept: application/json'   -H 'Content-Type: application/x-www-form-urlencoded'   -d 'grant_type=password&username=admin&password=ali&scope=&client_id=string&client_secret=string'
```
**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1Ni9.eyN30.09bJ0zo4YeOfSA-NOz2SCJfDeM-v8",
  "token_type": "bearer"
}
```

### 3. Upload Document (Admin Only)
```bash
curl -X 'POST'   'http://127.0.0.1:8000/v1/document/upload/'   -H 'accept: application/json'   -H 'Authorization: Bearer YOUR_JWT_AUTH_TOKEN'   -H 'Content-Type: multipart/form-data'   -F 'file=@sample_internal_document.txt;type=text/plain'
```
**Response:**
```json
{
  "message": "Document 'xyz.txt' added and vector store updated successfully."
}
```

### 4. Ask a Query
```bash
curl -X 'POST'   'http://127.0.0.1:8000/v1/query/ask/'   -H 'accept: application/json'   -H 'Content-Type: application/json'   -d '{
  "query": "How many rounds of interviews are there for ML engineers?"
}'
```
**Response:**
```json
{
  "answer": "There are 2 rounds of interviews for ML engineers",
  "sources": [
    {
      "source": "app/Documents/new_docs/xyz.txt",
      "chunk_index": 0,
      "text": "I hope this message finds you well.I am reaching out to you regarding your application for the ML Engineer position at XYZ. After carefully reviewing your profile, we are impressed with your skills and experience, and we would like to invite you to proceed with our interview process.Our interview process consists of two rounds, designed to assess your technical skills, problem-solving abilities, and cultural fit within our team. Here's an overview of what to expect:",
      "file_path": "app/Documents/new_docs/xyz.txt"
    }
  ]
}
```
