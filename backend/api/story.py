# backend/api/story.py
from fastapi import APIRouter
from typing import List
from db.schemas.story import StoryCreate, StoryUpdate, StoryRead
from db.schemas.episode import EpisodeRead  # 스토리별 에피소드 응답 스키마
from services.story_agent import (
    create_story, get_story_by_id, update_story, delete_story
)
from services.episode_agent import list_episodes_by_story  # 스토리별 에피소드 조회 로직


router = APIRouter()

@router.post("/stories", response_model=StoryRead)
def create(data: StoryCreate):
    return create_story(data)

@router.get("/stories/{story_id}", response_model=StoryRead)
def read(story_id: str):
    return get_story_by_id(story_id)

@router.put("/stories/{story_id}", response_model=StoryRead)
def update(story_id: str, data: StoryUpdate):
    return update_story(story_id, data)

@router.delete("/stories/{story_id}", response_model=str)
def delete(story_id: str):
    return delete_story(story_id)

# 스토리별 에피소드 조회 엔드포인트
@router.get(
    "/stories/{story_id}/episodes",
    response_model=List[EpisodeRead],
    summary="List Episodes by Story",
)
def list_episodes_for_story(story_id: str):
    return list_episodes_by_story(story_id)

