# Import necessary modules from FastAPI and the application
from fastapi import HTTPException, status  # Importing HTTPException for error handling and status for HTTP status codes

# Importing the service responsible for processing queries and schema for input validation
from app.services.query_service import process_query  # The service layer function that handles the main logic for processing a query
from app.schemas.query import AskQuery  # Pydantic model to validate the structure of the incoming query data


class QueryController:
    """
    QueryController is responsible for handling query-related operations, such as processing user queries
    to retrieve relevant information from the vector store.
    It mediates between the routers and the service layer.
    """

    @staticmethod
    async def ask_question(query_data: AskQuery):
        """
        Handles the query processing by sending the query to the vector store for retrieving relevant information.

        Args:
            query_data (AskQuery): The validated query data provided by the user, containing the question to be processed.

        Returns:
            dict: A response object containing the answer to the query and relevant source documents.

        Raises:
            HTTPException: Raises a 500 Internal Server Error if there's an issue while processing the query.
        """
        try:
            # Call the process_query service function to handle query processing and retrieve relevant information
            response = await process_query(query_data)
            return response
        except Exception as e:
            # Raise HTTP 500 Internal Server Error if an issue occurs while processing the query
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
