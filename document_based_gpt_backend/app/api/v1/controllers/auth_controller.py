# Import necessary classes and functions from FastAPI and the application

# Importing HTTPException for raising HTTP-related errors and status for HTTP status codes
from fastapi import HTTPException, status

# Importing OAuth2PasswordRequestForm for token-based authentication
from fastapi.security import OAuth2PasswordRequestForm

# Import the services responsible for user registration and login
from app.services.auth_service import register_user, login_user

# Import Pydantic schema for user registration data
from app.models.user import UserRegister


class AuthController:
    """
    AuthController handles user-related operations such as registration and login.
    It acts as a bridge between the routers and the service layer for authentication.
    """

    @staticmethod
    async def register_user(user_data: UserRegister):
        """
        Registers a new user in the system.

        Args:
            user_data (UserRegister): User registration data that includes username, password, role, and optional admin key.

        Returns:
            dict: A response message indicating successful registration or an error message.

        Raises:
            HTTPException: If there's any error during the registration process, a 400 Bad Request error is raised.
        """
        try:
            # Call the register_user function from auth_service to handle the registration process
            response = await register_user(user_data)
            return response
        except Exception as e:
            # Raise HTTP 400 Bad Request if an error occurs during registration
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    @staticmethod
    async def login_user(form_data: OAuth2PasswordRequestForm):
        """
        Logs in an existing user and generates a JWT token for authentication.

        Args:
            form_data (OAuth2PasswordRequestForm): Form data that includes username and password.

        Returns:
            dict: A dictionary containing the access token and its type (e.g., Bearer).

        Raises:
            HTTPException: If there's any error during login, a 401 Unauthorized error is raised.
        """
        try:
            # Call the login_user function from auth_service to handle the login process
            token = await login_user(form_data)
            return token
        except Exception as e:
            # Raise HTTP 401 Unauthorized if an error occurs during login
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
