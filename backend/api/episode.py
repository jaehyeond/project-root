from fastapi import APIRouter, HTTPException, Query, Body
from typing import Optional, List
from db.schemas.episode import EpisodeCreate, EpisodeRead, EpisodeUpdate
from services.episode_agent import (
    create_episode, get_episode_by_id,
    update_episode, delete_episode,
    list_episodes_by_story, update_episode_order
)
#from db.models.episode import Episode

router = APIRouter()

@router.post("/episodes", response_model=EpisodeRead)
def create(data: EpisodeCreate):
    return create_episode(data)

@router.get("/episodes/{episode_id}", response_model=EpisodeRead)
def read(episode_id: str):
    episode = get_episode_by_id(episode_id)
    if not episode:
        raise HTTPException(404, "Episode not found")
    return episode

@router.put("/episodes/{episode_id}", response_model=EpisodeRead)
def update(episode_id: str, data: EpisodeUpdate):
    return update_episode(episode_id, data)

@router.delete("/episodes/{episode_id}", response_model=str)
def delete(episode_id: str):
    return delete_episode(episode_id)


@router.get("/episodes", response_model=List[EpisodeRead])
def read_episodes(story_id: Optional[str] = Query(None)):
    return list_episodes_by_story(story_id)


@router.patch(
    "/episodes/{episode_id}/order",
    response_model=EpisodeRead,
    summary="Reorder Episode",
    description="특정 episode의 order 필드를 변경합니다."
)
def reorder_episode(
    episode_id: str,
    new_order: int = Body(
        ...,
        embed=True,
        gt=0,
        description="새로운 순서 값 (양의 정수)"
    )
):
  
    return update_episode_order(episode_id, new_order)















# @router.get("/episodes", response_model=List[EpisodeRead])
# def list_episodes(limit: Optional[int] = None):
#     qs = Episode.objects.limit(limit) if limit else Episode.objects
#     return [EpisodeRead(**ep.to_mongo().to_dict()) for ep in qs]
