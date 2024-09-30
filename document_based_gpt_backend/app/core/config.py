import os

# JWT Configuration
# SECRET_KEY = "my_jwt_secret_key_here"
SECRET_KEY = os.getenv("SECRET_KEY")
# ADMIN_KEY = "my_admin_key_here"
ADMIN_KEY = os.getenv("ADMIN_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DOCUMENT_DIRECTORY_PATH = "app/Documents"
VECTOR_STORE_PATH = "app/vector_store/"
