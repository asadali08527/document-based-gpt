# Document related Pydantic Schemas
from pydantic import BaseModel


class DocumentUploadResponse(BaseModel):
    message: str

