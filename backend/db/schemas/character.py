from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from db.mongodb import PyObjectId

# ✅ POST /characters 요청용 스키마 (사용자 입력용)
class CharacterCreate(BaseModel):
    name: str
    age: int
    role: str
    gender: str
    description: str

# ✅ GET /characters 응답용 스키마 (DB 조회 결과 반환용)
class CharacterRead(BaseModel):
    id: PyObjectId = Field(alias="_id")
    name: str
    age: int
    role: Optional[str] = None
    gender: Optional[str] = None
    description: Optional[str] = None

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
    }

class CharacterUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    role: Optional[str] = None
    gender: Optional[str] = None
    description: Optional[str] = None

