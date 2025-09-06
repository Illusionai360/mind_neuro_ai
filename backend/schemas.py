from pydantic import BaseModel
from typing import List
from datetime import datetime

class MessageOut(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class ChatCreateOut(BaseModel):
    id: int
    title: str

class ChatHistoryOut(BaseModel):
    id: int
    title: str
    created_at: datetime

class ChatThreadOut(BaseModel):
    chat_id: int
    messages: List[MessageOut]
