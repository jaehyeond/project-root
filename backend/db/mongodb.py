# backend/db/mongodb.py
from mongoengine import connect
import os
from dotenv import load_dotenv
from bson import ObjectId
from pydantic import GetCoreSchemaHandler
from pydantic_core import core_schema

load_dotenv()

def init_mongo():
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME")
    connect(db=db_name, host=mongo_uri, alias="default")
    print(f"✅ MongoDB 연결 완료: {mongo_uri} -> {db_name}")

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: type, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            python_schema=core_schema.is_instance_schema(cls),
            json_schema=core_schema.str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )