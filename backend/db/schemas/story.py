# backend/db/schemas/story.py
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from db.mongodb import PyObjectId


class StoryCreate(BaseModel):
    title: str
    synopsis: Optional[str] = None

class StoryUpdate(BaseModel):
    title: Optional[str] = None
    synopsis: Optional[str] = None

class StoryRead(BaseModel):
    id: PyObjectId = Field(alias="_id")
    title: str
    synopsis: Optional[str] = None

    model_config = {
        "arbitrary_types_allowed": True,
        "populate_by_name": True,
    }
