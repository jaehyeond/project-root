# backend/services/story_agent.py
from db.models.story import Story
from db.models.episode import Episode
from db.schemas.story import StoryCreate, StoryUpdate, StoryRead
from bson import ObjectId
from fastapi import HTTPException
from db.mongodb import PyObjectId  # Pydantic ObjectId wrapping

def create_story(data: StoryCreate) -> StoryRead:
    story = Story(**data.model_dump())
    story.save()
    # MongoDB _id를 PyObjectId로 래핑
    doc = story.to_mongo().to_dict()
    doc["_id"] = PyObjectId(doc["_id"])
    return StoryRead(**doc)

def get_story_by_id(story_id: str) -> StoryRead:
    if not ObjectId.is_valid(story_id):
        raise HTTPException(400, "Invalid story ID format")
    story = Story.objects(id=ObjectId(story_id)).first()
    if not story:
        raise HTTPException(404, "Story not found")
    # MongoDB _id를 PyObjectId로 래핑
    doc = story.to_mongo().to_dict()
    doc["_id"] = PyObjectId(doc["_id"])
    return StoryRead(**doc)

def update_story(story_id: str, data: StoryUpdate) -> StoryRead:
    if not ObjectId.is_valid(story_id):
        raise HTTPException(400, "Invalid story ID format")
    story = Story.objects(id=ObjectId(story_id)).first()
    if not story:
        raise HTTPException(404, "Story not found")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(story, field, value)
    story.save()
    # MongoDB _id를 PyObjectId로 래핑
    doc = story.to_mongo().to_dict()
    doc["_id"] = PyObjectId(doc["_id"])
    return StoryRead(**doc)

def delete_story(story_id: str) -> str:
    if not ObjectId.is_valid(story_id):
        raise HTTPException(400, "Invalid story ID format")
    story = Story.objects(id=ObjectId(story_id)).first()
    if not story:
        raise HTTPException(404, "Story not found")
    
    # 연결된 에피소드 일괄 삭제
    Episode.objects(story=story).delete()
    story.delete()
    return f"Deleted story {story_id} and its episodes deleted"
