# Query related Pydantic Schemas
from pydantic import BaseModel


class AskQuery(BaseModel):
    query: str
