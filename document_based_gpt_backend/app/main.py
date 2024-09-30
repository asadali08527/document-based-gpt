# Import FastAPI class to create the main app instance
from fastapi import FastAPI

# Import CORS middleware to allow cross-origin requests from front-end applications
from fastapi.middleware.cors import CORSMiddleware

# Import routers for different API endpoints (authentication, document upload, and query handling)
from app.api.v1.routers import auth_router, document_router, query_router

# Import logging configuration function to set up application-level logging
from app.core.logging_config import setup_logging

# Import the vector store service to manage vector-based storage and retrieval for document data
from app.services.vector_store_service import VectorStoreService

# Initialize the vector store service as a singleton
# This ensures that the vector store is created and available throughout the application's lifecycle
vector_service = VectorStoreService()

# Create a FastAPI application instance
app = FastAPI()

# Set up logging for the application
setup_logging()

# Add middleware to handle Cross-Origin Resource Sharing (CORS) for the front-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust according to your front-end's URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers to be sent from the front-end
)

# Register routers to handle requests for different API functionalities
# Each router is tied to a prefix and tag to organize endpoints by category

# Authentication router to handle user registration and token-based login
app.include_router(auth_router.router, prefix="/v1/auth", tags=["auth"])

# Document router to handle file upload and processing (admin-only access)
app.include_router(document_router.router, prefix="/v1/document", tags=["document"])

# Query router to handle user queries and retrieve responses from vector-based document data
app.include_router(query_router.router, prefix="/v1/query", tags=["query"])
