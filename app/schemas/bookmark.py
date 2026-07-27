from pydantic import BaseModel


class BookmarkResponse(BaseModel):
    id: int
    user_id: int
    post_id: int

    class Config:
        from_attributes = True


class BookmarkStatus(BaseModel):
    bookmarked: bool


class BookmarkCount(BaseModel):
    bookmarks: int