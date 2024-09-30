# Import necessary modules and classes from FastAPI for HTTP exceptions
from fastapi import HTTPException

# Import utility functions for query validation and processing
from app.utils.query_util import is_safe_content, is_negative_response

# Import schema for request validation
from app.schemas.query import AskQuery

# Import VectorStoreService for interacting with vector storage (FAISS)
from app.services.vector_store_service import VectorStoreService


def get_answer_from_query(query: str):
    """
    Retrieves an answer and relevant document sources based on the user's query.
    The answer is generated using a QA chain built on top of a vector store.

    Args:
        query (str): The user's question or query to be processed.

    Returns:
        dict: A dictionary containing:
            - "answer": The generated answer from the QA system.
            - "sources": A list of relevant document chunks with metadata.
    """
    # Initialize the vector store service
    vss = VectorStoreService()

    # Retrieve relevant documents and their scores using the vector store retriever
    source_docs_with_scores = vss.get_relevant_documents(query)

    # Set a relevance threshold to filter out irrelevant documents
    RELEVANCE_THRESHOLD = 0.20  # Can be fine-tuned based on your specific use case

    # Filter documents that meet or exceed the relevance threshold
    relevant_docs = [
        doc for doc, score in source_docs_with_scores if score >= RELEVANCE_THRESHOLD
    ]

    # Generate an answer using the QA chain from the vector store service
    result = vss.qa_chain.run(query)

    # If no relevant documents are found or the result indicates a negative response,
    # return the answer without any source context
    if not relevant_docs or is_negative_response(result):
        return {
            "answer": result,
            "sources": []
        }

    # Return the answer along with relevant document sources and metadata
    return {
        "answer": result,
        "sources": [
            {
                "source": doc.metadata["source"],
                "chunk_index": doc.metadata["chunk_index"],
                "text": doc.page_content,
                "file_path": f"{doc.metadata['source']}"
            }
            for doc in relevant_docs
        ]
    }


async def process_query(query_data: AskQuery):
    """
    Processes a user's query, performs content moderation, and retrieves a relevant answer.

    Args:
        query_data (AskQuery): The query data encapsulated in a Pydantic schema.

    Returns:
        dict: A dictionary containing the answer and related document sources if any.

    Raises:
        HTTPException: If an error occurs while processing the query or if content is deemed inappropriate.
    """
    try:
        # Extract the query string from the request data
        query = query_data.query

        # Check if the query contains any inappropriate content
        if not is_safe_content(query):
            return {
                "answer": "The question contains inappropriate content and cannot be processed.",
                "sources": []
            }

        # Retrieve the answer based on the query using the vector store
        return get_answer_from_query(query)

    except Exception as e:
        # Log the error for debugging purposes
        print(e)

        # Raise an HTTP 500 Internal Server Error if any exception occurs
        raise HTTPException(status_code=500, detail=str(e))
