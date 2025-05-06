# backend/api/character.py

from fastapi import APIRouter, HTTPException, status, Query
from db.schemas.character import CharacterCreate, CharacterRead, CharacterUpdate
from services.character_agent import create_character, get_character_by_id, get_all_characters, update_character, delete_character
from typing import List, Optional
from db.models.character import Character

router = APIRouter()

@router.post("/characters")
def create_char(data: CharacterCreate):
    return create_character(data)

@router.get("/characters/{character_id}", response_model=CharacterRead)
def read_character(character_id: str):
    character = get_character_by_id(character_id)
    if not character:
        raise HTTPException(status_code=404, detail="Character not found")
    return character

@router.get("/characters", response_model=List[CharacterRead])
def list_characters(
    name: Optional[str] = Query(None),
    age: Optional[int] = Query(None),
    gender: Optional[str] = Query(None),
    role: Optional[str] = Query(None),
    description: Optional[str] = Query(None)
):
    filters = {}
    if name:
        filters["name__icontains"] = name  # 부분 일치 검색
    if age:
        filters["age"] = age
    if gender:
        filters["gender__iexact"] = gender
    if role:
        filters["role__iexact"] = role
    if description:
        filters["description__icontains"] = description

    characters = Character.objects(**filters).order_by("-id")
    return [CharacterRead(**char.to_mongo().to_dict()) for char in characters]

@router.put("/characters/{character_id}", response_model=CharacterRead)
def update_char(character_id: str, data: CharacterUpdate):
    try:
        return update_character(character_id, data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/characters/{character_id}", response_model=str, status_code=status.HTTP_200_OK)
def delete_char(character_id: str):
    return delete_character(character_id)
