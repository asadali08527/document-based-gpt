# Import necessary modules from FastAPI
from fastapi import APIRouter

# Import schema and controller for query-related operations
from app.schemas.query import AskQuery
from app.api.v1.controllers.query_controller import QueryController

# Initialize the router for handling query endpoints
router = APIRouter()


@router.post("/ask/")
async def ask_question(query_data: AskQuery):
    """
    Handles a user query and returns an appropriate response based on document vector search.

    Args:
        query_data (AskQuery): The query input data containing the user's question.

    Returns:
        dict: A response containing the answer to the query and its associated sources (if any).

    Example:
        POST /v1/query/ask/
        JSON payload: { "query": "What is AI?" }

        Response:
        {
            "answer": "Artificial Intelligence (AI) is...",
            "sources": [
                {
                    "source": "filename.txt",
                    "chunk_index": 1,
                    "text": "Content related to AI...",
                    "file_path": "Documents/filename.txt"
                }
            ]
        }
    """
    # Use the QueryController to process the question and retrieve the response
    return await QueryController.ask_question(query_data)
