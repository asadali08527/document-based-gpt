# Import necessary modules from FastAPI
from fastapi import APIRouter, Depends  # APIRouter for routing logic, Depends for dependency injection
from fastapi.security import OAuth2PasswordRequestForm  # OAuth2PasswordRequestForm for handling form-based login

# Import the AuthController to handle authentication-related actions
from app.api.v1.controllers.auth_controller import AuthController  # Controller for handling authentication logic

# Import necessary schemas
from app.models.token import Token  # Schema for the token response model
from app.models.user import UserRegister  # Schema for validating user registration input

# Initialize the router for handling authentication endpoints
router = APIRouter()


@router.post("/register/")
async def register(user: UserRegister):
    """
    Registers a new user in the system.

    Args:
        user (UserRegister): The user registration data, validated by the UserRegister schema.

    Returns:
        dict: A success message indicating that the user has been registered.

    Example:
        POST /v1/auth/register/
        Payload: { "username": "john_doe", "password": "1234", "role": "user" }
    """
    # Call the AuthController to handle the user registration
    return await AuthController.register_user(user)


@router.post("/token/", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticates a user and generates a JWT access token.

    Args:
        form_data (OAuth2PasswordRequestForm): Form data containing 'username' and 'password'.

    Returns:
        Token: An access token that can be used for authenticated requests.

    Example:
        POST /v1/auth/token/
        Form data: { "username": "john_doe", "password": "1234" }
    """
    # Call the AuthController to handle user login and token generation
    return await AuthController.login_user(form_data)
