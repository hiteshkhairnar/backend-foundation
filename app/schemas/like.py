from pydantic import BaseModel


class LikeResponse(BaseModel):
    id: int
    user_id: int
    post_id: int

    class Config:
        from_attributes = True


class LikeCount(BaseModel):
    likes: int


class LikeStatus(BaseModel):
    liked: bool