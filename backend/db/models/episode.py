# backend/models/episode_agent.py

from mongoengine import Document, StringField, ReferenceField, IntField
from .story import Story  # Episode는 특정 Story에 속함

class Episode(Document):
    title = StringField(required=True)
    content = StringField(required=True)
    order = IntField(required=True)  # 몇 번째 에피소드인지 순서를 나타냄
    story = ReferenceField(Story, required=True)  # 어떤 스토리에 속하는지

    meta = {"collection": "episodes"}
