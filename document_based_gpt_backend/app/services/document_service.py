# Import UploadFile from FastAPI to handle file uploads
from fastapi import UploadFile

# Import configurations for file paths from the core config module
from app.services.vector_store_service import VectorStoreService


async def add_document(file: UploadFile):
    """
    Adds a new document to the vector store by saving it, processing it,
    and updating the vector index.

    Args:
        file (UploadFile): The file to be added to the vector store.

    Returns:
        dict: A success message indicating that the document was added and vector store updated.
    """

    vss = VectorStoreService()
    return {"message": await vss.add_document_to_vector_store(file)}

