from typing import List, Dict, Any, Optional
from app.core.database import supabase_client

class SuccessStoryService:
    @staticmethod
    async def create_story(story_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new success story
        """
        response = supabase_client.table("success_stories").insert(story_data).execute()
        if len(response.data) > 0:
            return response.data[0]
        raise ValueError("Failed to create success story")

    @staticmethod
    async def get_story(story_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a success story by ID
        """
        response = supabase_client.table("success_stories").select("*").eq("story_id", story_id).execute()
        if len(response.data) > 0:
            return response.data[0]
        return None

    @staticmethod
    async def get_all_stories() -> List[Dict[str, Any]]:
        """
        Get all success stories
        """
        response = supabase_client.table("success_stories").select("*").order("published_at", desc=True).execute()
        return response.data

    @staticmethod
    async def update_story(story_id: int, story_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update a success story
        """
        response = supabase_client.table("success_stories").update(story_data).eq("story_id", story_id).execute()
        if len(response.data) > 0:
            return response.data[0]
        return None

    @staticmethod
    async def delete_story(story_id: int) -> bool:
        """
        Delete a success story
        """
        response = supabase_client.table("success_stories").delete().eq("story_id", story_id).execute()
        return len(response.data) > 0
