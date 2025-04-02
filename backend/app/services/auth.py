from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional, Dict, Any
from app.core.config import get_settings
from app.db.supabase_client import supabase_manager
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, TokenData

settings = get_settings()

class AuthService:
    """Service for handling authentication operations."""
    
    @staticmethod
    async def register_user(user_data: UserCreate) -> User:
        """
        Register a new user in the system.
        
        Args:
            user_data: User registration data
            
        Returns:
            User: The newly created user
        
        Raises:
            HTTPException: If registration fails
        """
        try:
            # Prepare user metadata
            user_metadata = {
                "username": user_data.username,
                "full_name": user_data.full_name,
                "phone_number": user_data.phone_number,
                "address": user_data.address,
                "additional_info": user_data.additional_info or {}
            }
            
            # Register user with Supabase
            response = await supabase_manager.sign_up(
                email=user_data.email,
                password=user_data.password,
                user_metadata=user_metadata
            )
            
            # Extract user data from response
            user_data = response.user
            if not user_data:
                raise ValueError("User registration failed")
            
            # Create User model instance
            user = User.from_supabase(user_data)
            
            return user
            
        except Exception as e:
            raise
    
    @staticmethod
    async def authenticate_user(credentials: UserLogin) -> Optional[User]:
        """
        Authenticate a user with email and password.
        
        Args:
            credentials: User login credentials
            
        Returns:
            Optional[User]: Authenticated user or None if authentication fails
        """
        try:
            # Attempt to sign in with Supabase
            response = await supabase_manager.sign_in(
                email=credentials.email,
                password=credentials.password
            )
            
            # Check if authentication was successful
            if not response.user:
                return None
            
            # Create User model instance
            user = User.from_supabase(response.user)
            
            return user
            
        except Exception as e:
            return None
    
    @staticmethod
    async def get_current_user(token: str) -> Optional[User]:
        """
        Get the current user from a JWT token.
        
        Args:
            token: JWT token
            
        Returns:
            Optional[User]: User information or None if token is invalid
        """
        try:
            # Get user from Supabase using the token
            response = supabase_manager.get_user(token)
            
            if not response or not response.user:
                return None
                
            # Create User model instance
            user = User.from_supabase(response.user)
            return user
            
        except Exception as e:
            return None
    
    @staticmethod
    def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token.
        
        Args:
            data: Data to encode in the token
            expires_delta: Token expiration time
            
        Returns:
            str: Encoded JWT token
        """
        to_encode = data.copy()
        
        # Set expiration time
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
            
        to_encode.update({"exp": expire})
        
        # Create JWT token
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.JWT_SECRET, 
            algorithm=settings.JWT_ALGORITHM
        )
        
        return encoded_jwt