# Import necessary modules from FastAPI for dependency injection and HTTP error handling
from fastapi import Depends, HTTPException

# Import OAuth2PasswordBearer for token-based authentication
from fastapi.security import OAuth2PasswordBearer

# Import JWTError and jwt from the `jose` package for handling JWT-based authentication and token operations
from jose import JWTError, jwt

# Import a mock database to store user data
from app.db.mock_database import users_db

# Import application-level configuration, such as secrets and algorithm
from app.core import config

# Define the OAuth2 scheme for bearer token authentication
# `tokenUrl` is the URL path where the token will be generated
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Retrieve the current user based on the JWT token provided.

    Args:
        token (str): The access token provided in the Authorization header.

    Returns:
        dict: A dictionary containing user details.

    Raises:
        HTTPException: If the token is invalid or the user is not found.
    """
    try:
        # Decode the JWT token using the secret key and algorithm
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])

        # Extract user information from the payload
        username: str = payload.get("sub")
        role: str = payload.get("role")

        # If username or role is missing, raise an authentication error
        if username is None or role is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Retrieve the user from the database using the username
        user = users_db.get(username)

        # If the user is not found, raise an authentication error
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Return the authenticated user's details
        return user

    except JWTError:
        # Handle any errors related to token decoding or validation
        raise HTTPException(status_code=401, detail="Invalid credentials")


async def is_admin_user(current_user: dict = Depends(get_current_user)):
    """
    Verify that the current user has an admin role.

    Args:
        current_user (dict): The user details obtained from the `get_current_user`.

    Returns:
        dict: A dictionary containing user details if the user is an admin.

    Raises:
        HTTPException: If the user is not authorized as an admin.
    """
    # Check if the role of the current user is 'admin'
    if current_user["role"] != "admin":
        # If not, raise a "Forbidden" error
        raise HTTPException(status_code=403, detail="Not authorized")

    # Return the current user's details if they are authorized as an admin
    return current_user
