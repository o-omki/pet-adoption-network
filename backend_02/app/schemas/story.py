from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class StoryBase(BaseModel):
    pet_id: str
    adopter_id: str
    story_title: str
    story_content: str
    image_url: Optional[str] = None


class StoryCreate(StoryBase):
    pass


class StoryUpdate(BaseModel):
    story_title: Optional[str] = None
    story_content: Optional[str] = None
    image_url: Optional[str] = None


class StoryInDB(StoryBase):
    story_id: str
    published_at: datetime

    class Config:
        orm_mode = True


class StoryResponse(StoryInDB):
    pass
