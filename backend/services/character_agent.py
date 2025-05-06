# backend/services/character_agent.py

from db.models.character import Character
from db.schemas.character import CharacterCreate, CharacterRead, CharacterUpdate
from typing import List, Optional
from bson import ObjectId
from fastapi import HTTPException
from db.mongodb import PyObjectId  # Pydantic ObjectId wrapping

def create_character(data: CharacterCreate):
    char = Character(**data.model_dump())
    char.save()
    doc = char.to_mongo().to_dict()
    # MongoDB _id를 PyObjectId로 래핑
    doc["_id"] = PyObjectId(doc["_id"])
    return CharacterRead(**doc)

def get_character_by_id(character_id: str) -> Optional[CharacterRead]:
    # ObjectId 검증
    if not ObjectId.is_valid(character_id):
        return None

    # 단일 조회 및 예외 처리
    try:
        char = Character.objects.get(id=ObjectId(character_id))
    except Exception:
        return None

    # MongoDB _id를 PyObjectId로 래핑
    doc = char.to_mongo().to_dict()
    doc["_id"] = PyObjectId(doc["_id"])
    return CharacterRead(**doc)

# 전체 캐릭터 목록 조회 서비스 함수
def get_all_characters() -> List[CharacterRead]:
    characters = Character.objects().order_by('-id')
    result = []
    for c in characters:
        doc = c.to_mongo().to_dict()
        doc["_id"] = PyObjectId(doc["_id"])
        result.append(CharacterRead(**doc))
    return result

# 캐릭터 정보 수정
def update_character(character_id: str, data: CharacterUpdate) -> CharacterRead:
    char = Character.objects(id=character_id).first()
    if not char:
        raise ValueError("Character not found")

    update_data = data.model_dump(exclude_unset=True)  # Pydantic v2 기준
    for field, value in update_data.items():
        setattr(char, field, value)

    char.save()
    doc = char.to_mongo().to_dict()
    doc["_id"] = PyObjectId(doc["_id"])
    return CharacterRead(**doc)

#캐릭터 삭제 서비스 함수
def delete_character(char_id: str) -> str:
    # 1) ObjectId 유효성 검증
    if not ObjectId.is_valid(char_id):
        raise HTTPException(status_code=404, detail="Invalid character ID format")

    # 2) 문서 존재 여부 확인
    char = Character.objects(id=ObjectId(char_id)).first()
    if not char:
        raise HTTPException(status_code=404, detail="Character not found")

    # 3) 삭제 수행
    char.delete()
    return f"Character with id {char_id} deleted successfully."
#dddddd


