# backend/main.py
from fastapi import FastAPI
from db.mongodb import init_mongo
from api.character import router as character_router
from api.story import router as story_router
from api.episode import router as episode_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_mongo()
    yield

app = FastAPI(title="Character API", version="1.0.0", lifespan=lifespan)

# 라우터 등록
app.include_router(character_router)
app.include_router(story_router)
app.include_router(episode_router)

