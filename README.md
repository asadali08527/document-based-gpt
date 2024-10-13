
# Document-Based GPT System

## Project Overview
The Document-Based GPT System is a backend and frontend solution designed to enable users to query document contents and receive precise answers from an AI system. The core functionality includes secure user authentication, document upload, and vector store creation using embeddings to enhance searchability. The frontend interacts with the backend to allow users to register, log in, upload documents (admin only), and query for information.

## Approach Taken

### Backend
The backend was built using **FastAPI**, a modern, fast web framework for building APIs with Python 3.6+ based on standard Python type hints. To handle secure authentication and user roles, JWT-based token management was used with `fastapi-users`. The document processing, vector store creation, and querying functionalities were handled using **LangChain** and **FAISS** for vector storage. **OpenAI embeddings** were utilized for efficient document searching based on content.

Key Features Implemented:
1. **Authentication & Authorization**: Role-based authentication allowing normal users to query documents and admin users to upload documents and manage vector stores.
2. **Document Upload & Processing**: Uploaded documents are split into manageable chunks and indexed using vector embeddings for efficient querying.
3. **Query & Response**: Users can query the vector store, and the system retrieves the most relevant document chunks and provides answers.

### Frontend
The frontend was built using **React**, allowing for a responsive and intuitive interface for users to interact with the backend API. Users can:
1. **Register & Log in**: Sign up as a user or admin, requiring an admin key for admin registration.
2. **Upload Documents (Admin Only)**: Allows admin users to securely upload documents.
3. **Query the System**: All users can query the document contents for relevant information.

## Tech Stack & Libraries

### Backend Libraries
- **FastAPI & Uvicorn**: API framework and ASGI server for rapid development and deployment.
- **OpenAI, LangChain, FAISS**: For embeddings, vector storage, and document operations.
- **JWT, Passlib, Cryptography**: For secure token-based authentication and hashing.
- **Better Profanity, Bcrypt**: Content filtering and authentication utilities.
- **Python-Multipart, Transformers, Tiktoken, Unstructured**:
  - **Python-Multipart**: Handle file uploads.
  - **Transformers**: Provides NLP-based utilities and support for OpenAI integrations.
  - **Tiktoken**: Token management for NLP operations.
  - **Unstructured**: Handles diverse document formats for extraction and processing.
- **Python-Magic**: Identifies file types and assists with document processing.

### Frontend Libraries
- **React & React-DOM**: Core libraries for creating the user interface.
- **Axios**: For making HTTP requests to the backend API.
- **React Scripts**: For running and building the frontend application.

## Project Directory Structure

### Backend
- **api/v1**: API routers and controllers for modular request handling.
- **core**: Configuration and logging setup.
- **db**: Handles vector store operations using FAISS.
- **models & schemas**: Defines Pydantic models for request/response validation.
- **services**: Implements business logic for vector store operations, query processing, and authentication.
- **utils**: Utility functions for document processing, authentication, and query utilities.

### Frontend
- **public**: Public assets like HTML and icons.
- **src**: Main application code including components for authentication, chatbox, and document upload.

## Key Classes & Methods

### Backend
- **VectorStoreService**: Handles vector store creation, updating, and querying. Manages OpenAI embeddings and document storage using FAISS.
- **AuthController & DocumentController**: Handle API endpoints for authentication and document upload.
- **get_answer_from_query()**: Retrieves answers based on vector store search for user queries.

### Frontend
- **App.js**: Main component handling routing, authentication, and conditional rendering based on user role.
- **ChatBox**: Allows users to query the backend and displays the response.
- **UploadDocument**: Allows admin users to upload files to the backend.

## Running the Solution

### Docker Setup
1. Ensure the `.env` file contains:
    ```
    ADMIN_KEY=my_admin_key_here
    SECRET_KEY=my_jwt_secret_key_here
    OPENAI_API_KEY=your_openai_api_key
    ```
2. Build and run the backend:
   ```
   docker build -t document_based_gpt_backend:latest .
   docker run -p 8000:8000 --env-file .env document_based_gpt_backend:latest
   ```
   Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to interact with the API.

3. Build and run the frontend:
   ```
   docker build -t document-gpt-client:latest .
   docker run -p 3000:3000 document-gpt-client:latest
   ```
   Visit [http://localhost:3000](http://localhost:3000).

### Virtual Environment Setup (Non-Docker)
1. Create a virtual environment:
   ```
   python -m venv env
   source env/bin/activate  # On Windows: env\Scriptsctivate
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the backend:
   ```
   uvicorn app.main:app --reload
   ```
4. Navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for API docs.

### API Usage Examples

1. **Register User as Admin/User**:
   ```sh
   curl -X 'POST'    'http://127.0.0.1:8000/v1/auth/register/'    -H 'Content-Type: application/json'    -d '{"username": "admin", "password": "testpassword", "role": "admin", "admin_key": "admin_key_here"}'
   ```

2. **Login & Get Token**:
   ```sh
   curl -X 'POST'    'http://127.0.0.1:8000/v1/auth/token/'    -H 'Content-Type: application/x-www-form-urlencoded'    -d 'grant_type=password&username=admin&password=testpassword'
   ```

3. **Upload Document (Admin Only)**:
   ```sh
   curl -X 'POST'    'http://127.0.0.1:8000/v1/document/upload/'    -H 'Authorization: Bearer YOUR_JWT_AUTH_TOKEN'    -F 'file=@document.txt;type=text/plain'
   ```

4. **Query the Document**:
   ```sh
   curl -X 'POST'    'http://127.0.0.1:8000/v1/query/ask/'    -H 'Content-Type: application/json'    -d '{"query": "What is the content of the document?"}'
   ```

## Challenges & Solutions

1. **Handling Large Documents**: Splitting documents into chunks for vector storage was necessary for efficient retrieval.
   - Solution: Used `RecursiveCharacterTextSplitter` to break down large documents.
   
2. **Content Moderation**: Ensuring user queries do not contain inappropriate content.
   - Solution: Integrated `better_profanity` for text filtering.

3. **Efficient Vector Storage & Search**: Optimizing search over document content using vector embeddings.
   - Solution: Utilized FAISS for fast similarity searches on vector embeddings.

4. **Authentication & Role-Based Access**: Ensuring secure access for users and admins.
   - Solution: Implemented JWT-based authentication, with role checks for sensitive actions like uploading documents.

## Conclusion
The Document-Based GPT System is a scalable and efficient solution for content querying over large document repositories. It leverages AI-powered embeddings, vector stores, and role-based access control to provide a robust platform for document-based question-answering.
