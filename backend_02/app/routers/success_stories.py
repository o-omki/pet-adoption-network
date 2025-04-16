from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Any
from datetime import datetime

from app.schemas.story import StoryCreate, StoryUpdate, StoryResponse
from app.services.success_story_service import SuccessStoryService
from app.core.auth import get_current_user

router = APIRouter()


@router.post("", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_story(story_data: StoryCreate, current_user: dict = Depends(get_current_user)) -> Any:
    """
    Submit a new success story.
    """
    # Check if the current user is the adopter
    if story_data.adopter_id != current_user.get("user_id"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only submit success stories for your own adoptions"
        )
    
    # Add published_at timestamp
    story_dict = story_data.dict()
    story_dict["published_at"] = datetime.utcnow().isoformat()
    
    try:
        created_story = await SuccessStoryService.create_story(story_dict)
        return {
            "message": "Story submitted successfully",
            "story_id": created_story.get("story_id")
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("", response_model=List[StoryResponse])
async def get_all_stories() -> Any:
    """
    Retrieve all success stories.
    """
    return await SuccessStoryService.get_all_stories()


@router.get("/{story_id}", response_model=StoryResponse)
async def get_story(story_id: int) -> Any:
    """
    Retrieve a specific success story.
    """
    story = await SuccessStoryService.get_story(story_id)
    if not story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Story not found"
        )
    return story


@router.put("/{story_id}", response_model=StoryResponse)
async def update_story(
    story_id: int,
    story_update: StoryUpdate,
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Update a success story (allowed for the story owner or admin).
    """
    # Fetch the existing story
    existing_story = await SuccessStoryService.get_story(story_id)
    if not existing_story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Story not found"
        )
    
    # Check permissions: only the adopter who created the story or an admin can update it
    if current_user.get("user_id") != existing_story.get("adopter_id") and current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to update this story"
        )
    
    # Update only provided fields
    update_data = {k: v for k, v in story_update.dict().items() if v is not None}
    
    updated_story = await SuccessStoryService.update_story(story_id, update_data)
    if not updated_story:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update story"
        )
    
    return updated_story


@router.delete("/{story_id}", status_code=status.HTTP_200_OK)
async def delete_story(
    story_id: int,
    current_user: dict = Depends(get_current_user)
) -> Any:
    """
    Delete a success story (allowed for the story owner or admin).
    """
    # Fetch the existing story
    existing_story = await SuccessStoryService.get_story(story_id)
    if not existing_story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Story not found"
        )
    
    # Check permissions: only the adopter who created the story or an admin can delete it
    if current_user.get("user_id") != existing_story.get("adopter_id") and current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to delete this story"
        )
    
    success = await SuccessStoryService.delete_story(story_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete story"
        )
    
    return {"message": "Story deleted successfully"}
