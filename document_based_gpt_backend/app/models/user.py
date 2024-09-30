# Pydantic User Schema
from pydantic import BaseModel


# User BaseModel for Pydantic
class UserRegister(BaseModel):
    username: str
    password: str
    role: str  # 'admin' or 'user'
    admin_key: str = None  # Optional for admins
