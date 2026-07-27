from pydantic import BaseModel
from datetime import datetime


class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    content: str
    user_id: int
    post_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CommentOwner(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class CommentWithOwner(BaseModel):
    id: int
    content: str
    created_at: datetime

    owner: CommentOwner

    class Config:
        from_attributes = True