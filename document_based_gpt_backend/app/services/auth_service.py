# Import required modules for handling time-related operations
from datetime import timedelta

# Import FastAPI exception handling to return HTTP responses with specific status codes and messages
from fastapi import HTTPException

# Import utility functions for security-related operations like authentication, password hashing, and token creation
from app.utils.security_util import authenticate_user, hash_password, create_access_token

# Import the UserRegister model to validate user registration data
from app.models.user import UserRegister

# Import a mock database to store users in-memory for simplicity (should be replaced with real database in production)
from app.db.mock_database import users_db

# Import configuration settings such as the admin key, token expiration, etc.
from app.core import config


async def register_user(user: UserRegister):
    """
    Registers a new user (admin or regular user) into the mock database.

    Args:
        user (UserRegister): User registration data.

    Returns:
        dict: Success message indicating the user has been registered.

    Raises:
        HTTPException: If the user already exists or admin key is invalid.
    """
    # Check if the username already exists in the database
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="User already exists")

    # If the user role is 'admin', validate the provided admin key
    if user.role == "admin" and user.admin_key != config.ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin key")

    # Hash the user's password for secure storage
    hashed_password = hash_password(user.password)

    # Store the user data (hashed password and role) in the mock database
    users_db[user.username] = {"username": user.username, "hashed_password": hashed_password, "role": user.role}

    # Return a success message upon registration
    return {"message": "User registered successfully"}


async def login_user(form_data):
    """
    Authenticates the user and generates a JWT token upon successful login.

    Args:
        form_data (OAuth2PasswordRequestForm): Form data containing username and password.

    Returns:
        dict: Access token and token type if login is successful.

    Raises:
        HTTPException: If username/password is incorrect.
    """
    # Authenticate the user using the provided username and password
    user = authenticate_user(form_data.username, form_data.password)

    # If the authentication fails, raise an error
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    # Set the token expiration time as defined in the configuration
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)

    # Create a JWT access token with the user's username and role
    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"]},
        expires_delta=access_token_expires
    )

    # Return the access token and its type
    return {"access_token": access_token, "token_type": "bearer"}
