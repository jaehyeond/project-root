# backend/schemas/episode_agent.py

from pydantic import BaseModel, Field
from typing import Optional
from db.mongodb import PyObjectId

class EpisodeCreate(BaseModel):
    title: str
    content: str
    order: int
    story_id: str  # 어떤 Story에 속하는지

class EpisodeRead(BaseModel):
    id: PyObjectId = Field(alias="_id")
    title: str
    content: str
    order: int
    story_id: str

    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True,
    }

class EpisodeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    order: Optional[int] = None
