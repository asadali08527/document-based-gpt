# Security-related utility functions
# Handles password hashing, verification, user authentication, and token generation.

from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt
from app.core import config
from app.db.mock_database import users_db

# Initialize a password context for bcrypt hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hash the password
def hash_password(password: str) -> str:
    """
    Hashes a plain-text password using bcrypt algorithm.

    Args:
        password (str): The plain-text password to be hashed.

    Returns:
        str: A hashed password that can be safely stored in the database.
    """
    return pwd_context.hash(password)


# Verify if the password is correct
def verify_password(plain_password, hashed_password):
    """
    Verifies if a plain-text password matches the hashed password.

    Args:
        plain_password (str): The plain-text password provided by the user.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: `True` if the password matches, otherwise `False`.
    """
    return pwd_context.verify(plain_password, hashed_password)


# Authenticate user against mock database
def authenticate_user(username: str, password: str):
    """
    Authenticates a user against the mock user database.

    This function retrieves a user's information from the mock database,
    verifies the provided password, and returns the user data if authentication is successful.

    Args:
        username (str): The username of the user.
        password (str): The plain-text password provided by the user.

    Returns:
        dict or None: User information if authentication is successful, otherwise `None`.
    """
    # Retrieve user data from the mock database
    user = users_db.get(username)
    # Check if user exists and the password is valid
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    return user


# Create a JWT token for user authentication
def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Creates a JWT access token for the authenticated user.

    This function generates a JWT token with the provided data and an optional expiration time.
    The token is signed using the application's secret key and algorithm for secure transmission.

    Args:
        data (dict): A dictionary containing the user's information and claims for the token.
        expires_delta (timedelta, optional): The time delta for the token's expiration.

    Returns:
        str: A JWT access token.
    """
    # Create a copy of the data to be encoded into the token
    to_encode = data.copy()
    # Set expiration time for the token
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    # Encode the data into a JWT token using the secret key and algorithm
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
