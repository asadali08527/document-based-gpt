# Import necessary modules from FastAPI and the application

# Importing HTTPException for error handling, UploadFile for file upload handling, and status for HTTP status codes
from fastapi import HTTPException, UploadFile, status
# Importing the service function responsible for document upload and processing
from app.services.document_service import add_document


class DocumentController:
    """
    DocumentController handles document-related operations such as uploading and processing.
    It acts as a mediator between routers and the service layer for document management.
    """

    @staticmethod
    async def upload_document(file: UploadFile):
        """
        Uploads a document to the vector store and updates the stored index for querying.

        Args:
            file (UploadFile): The file to be uploaded, expected to be a text document.

        Returns:
            dict: A response message indicating that the document was uploaded and indexed successfully.

        Raises:
            HTTPException: Raises a 500 Internal Server Error if there's an issue while uploading or processing the document.
        """
        try:
            # Call the add_document service function to handle document upload and processing
            response = await add_document(file)
            return response
        except Exception as e:
            # Raise HTTP 500 Internal Server Error if an issue occurs while processing the file upload
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
