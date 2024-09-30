# Import necessary modules from FastAPI
from fastapi import APIRouter, UploadFile, File, Depends

# Import the DocumentController to handle document-related actions
from app.api.v1.controllers.document_controller import DocumentController

# Import utility function to verify admin user access
from app.utils.auth_util import is_admin_user

# Initialize the router for handling document endpoints
router = APIRouter()


@router.post("/upload/")
async def upload_document(file: UploadFile = File(...), current_user: dict = Depends(is_admin_user)):
    """
    Uploads a document to the system and updates the vector store.

    Args:
        file (UploadFile): The file to be uploaded, validated by FastAPI's UploadFile type.
        current_user (dict): The current authenticated user, automatically injected by the `is_admin_user` dependency.

    Returns:
        dict: A message indicating the success of the upload and update process.

    Example:
        POST /v1/document/upload/
        Form data: { file: [File] }

        Response:
        { "message": "Document 'filename.txt' added and vector store updated successfully." }
    """
    # Call the DocumentController to handle the file upload
    return await DocumentController.upload_document(file)
