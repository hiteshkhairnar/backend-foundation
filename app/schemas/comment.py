from pydantic import BaseModel


class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    content: str
    user_id: int
    post_id: int

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

    owner: CommentOwner

    class Config:
        from_attributes = True