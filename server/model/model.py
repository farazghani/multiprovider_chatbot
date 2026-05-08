from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime , timezone
import uuid


class User(BaseModel):
    id : str
    name: str = Field(min_length=3 , max_length=20 , description="username cant be less than 3and greater than 20")
    email: str
    password: str = Field(min_length=3 , max_length=30)
    jwt: Optional[str] = None

class Userresponse(BaseModel):
     id: Optional[str] = None
     jwt: Optional[str] = None
     success: bool
     error: Optional[str] = None

    

class ChatMessage(BaseModel):
    role: Literal[
        "system",
        "user",
        "assistant",
        "tool"
    ]
    content: str
    created_At: datetime = Field(default_factory=datetime.utcnow)
    provider: Optional[str] = None



class Conversation(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    title: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class ConversationResponse(Conversation):
    messages: list[ChatMessage] = []

