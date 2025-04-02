from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Any, Dict
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token
from app.services.auth import AuthService

router = APIRouter(tags=["auth"])

# OAuth2 password bearer for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserCreate) -> Any:
    """
    Register a new user.
    
    Args:
        user_data: User registration data
        
    Returns:
        UserResponse: The newly created user information
    """
    try:
        user = await AuthService.register_user(user_data)
        return user.to_dict()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Registration failed. Please check your information and try again."
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again later."
        )

@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    Login endpoint that returns a JWT token.
    
    Args:
        form_data: OAuth2 password form containing username (email) and password
        
    Returns:
        Token: JWT access token
    """
    user_login = UserLogin(email=form_data.username, password=form_data.password)
    
    user = await AuthService.authenticate_user(user_login)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_data = {
        "sub": user.user_id,
        "email": user.email
    }
    access_token = AuthService.create_access_token(data=access_token_data)
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)) -> Dict[str, str]:
    """
    Logout a user by invalidating their token.
    
    Args:
        token: JWT token from authorization header
        
    Returns:
        Dict: Success message
    """
    try:
        await AuthService.get_current_user(token)
        return {"message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during logout"
        )

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """
    Get the current authenticated user.
    
    Args:
        token: JWT token from authorization header
        
    Returns:
        Dict: Authenticated user information
    """
    user = await AuthService.get_current_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user.to_dict()