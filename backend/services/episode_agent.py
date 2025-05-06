from typing import List, Optional
from bson import ObjectId
from db.models.episode import Episode
from db.schemas.episode import EpisodeCreate, EpisodeRead, EpisodeUpdate
from fastapi import HTTPException, status
from db.mongodb import PyObjectId  # Pydantic ObjectId wrapping


# ✅ Create
def create_episode(data: EpisodeCreate) -> EpisodeRead:
    # story_id를 story 필드로 매핑
    payload = data.model_dump()
    story_id = payload.pop("story_id")
    if not ObjectId.is_valid(story_id):
        raise HTTPException(status_code=400, detail="Invalid story ID format")
    payload["story"] = ObjectId(story_id)
    episode = Episode(**payload)
    episode.save()
    # MongoDB 문서를 dict로 변환
    doc = episode.to_mongo().to_dict()
    # _id와 story 필드를 Pydantic 스키마가 기대하는 형식으로 매핑
    doc["_id"] = PyObjectId(doc["_id"])
    doc["story_id"] = str(doc.pop("story"))
    return EpisodeRead(**doc)

# ✅ Read
def get_episode_by_id(episode_id: str) -> Optional[EpisodeRead]:
    if not ObjectId.is_valid(episode_id):
        return None
    episode = Episode.objects(id=ObjectId(episode_id)).first()
    if not episode:
        return None
    # MongoDB 문서를 dict로 변환
    doc = episode.to_mongo().to_dict()
    # _id와 story 필드를 Pydantic 스키마가 기대하는 형식으로 매핑
    doc["_id"] = PyObjectId(doc["_id"])
    doc["story_id"] = str(doc.pop("story"))
    return EpisodeRead(**doc)

# ✅ Update
def update_episode(episode_id: str, data: EpisodeUpdate) -> EpisodeRead:
    if not ObjectId.is_valid(episode_id):
        raise HTTPException(status_code=400, detail="Invalid episode ID format")

    episode = Episode.objects(id=ObjectId(episode_id)).first()
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(episode, field, value)
    episode.save()
    # MongoDB 문서를 dict로 변환
    doc = episode.to_mongo().to_dict()
    # _id와 story 필드를 Pydantic 스키마가 기대하는 형식으로 매핑
    doc["_id"] = PyObjectId(doc["_id"])
    doc["story_id"] = str(doc.pop("story"))
    return EpisodeRead(**doc)

# ✅ Delete
def delete_episode(episode_id: str) -> str:
    if not ObjectId.is_valid(episode_id):
        raise HTTPException(status_code=400, detail="Invalid episode ID format")
    episode = Episode.objects(id=ObjectId(episode_id)).first()
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")

    episode.delete()
    return f"Episode {episode_id} deleted successfully"

# ✅ List(분기기)
def list_episodes_by_story(story_id: Optional[str] = None) -> List[EpisodeRead]:
    if story_id:
        if not ObjectId.is_valid(story_id):
            raise HTTPException(status_code=400, detail="Invalid story ID format")
        qs = Episode.objects(story=ObjectId(story_id))
    else:
        qs = Episode.objects()
    result = []
    for ep in qs:
        doc = ep.to_mongo().to_dict()
        # _id와 story 필드를 Pydantic 스키마가 기대하는 형식으로 매핑
        doc["_id"] = PyObjectId(doc["_id"])
        doc["story_id"] = str(doc.pop("story"))
        result.append(EpisodeRead(**doc))
    return result


# ✅ 순서변경 로직직
def update_episode_order(episode_id: str, new_order: int) -> EpisodeRead:
    if not ObjectId.is_valid(episode_id):
        raise HTTPException(status_code=400, detail="Invalid episode ID format")
    episode = Episode.objects(id=ObjectId(episode_id)).first()
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    episode.order = new_order
    episode.save()
    # MongoDB 문서를 dict로 변환
    doc = episode.to_mongo().to_dict()
    # _id와 story 필드를 Pydantic 스키마가 기대하는 형식으로 매핑
    doc["_id"] = PyObjectId(doc["_id"])
    doc["story_id"] = str(doc.pop("story"))
    return EpisodeRead(**doc)
