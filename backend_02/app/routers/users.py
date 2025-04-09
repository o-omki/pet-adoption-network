from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.auth import get_current_user
from app.services.user_service import UserService
from app.schemas.user import UserInDB, UserProfile

router = APIRouter()


@router.get("/me", response_model=dict)
async def read_current_user(current_user: dict = Depends(get_current_user)) -> Any:
    """
    Get the current authenticated user.
    """
    user_id = current_user.get("user_id")
    user = await UserService.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Remove the password field from the response
    user.pop("password", None)
    
    # Get the user's profile
    profile = await UserService.get_user_profile(user_id)
    profile = profile if profile else {}
    
    return {"user": user, "profile": profile}


@router.get("/{user_id}", response_model=dict)
async def get_user(user_id: str, current_user: dict = Depends(get_current_user)) -> Any:
    """
    Get a specific user by ID.
    """
    user = await UserService.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Remove the password field from the response
    user.pop("password", None)
    
    # Get the user's profile
    profile = await UserService.get_user_profile(user_id)
    profile = profile if profile else {}
    
    return {"user": user, "profile": profile}


@router.put("/{user_id}", response_model=dict)
async def update_user(
    user_id: str,
    profile: UserProfile,
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Update a user's profile.
    """
    # Check if the current user is the same as the one being updated
    if current_user.get("user_id") != user_id:
        # Check if the current user is an admin
        if current_user.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
    
    # Check if the user exists
    user = await UserService.get_user_by_id(user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update the user profile using the service
    try:
        profile_data = profile.dict(exclude_unset=True)
        await UserService.update_user_profile(user_id, profile_data)
        return {"message": "User profile updated successfully"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
