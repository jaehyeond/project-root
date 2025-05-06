# backend/db/models/story.py
from mongoengine import Document, StringField

class Story(Document):
    title = StringField(required=True)
    synopsis = StringField()
