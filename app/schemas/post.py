from pydantic import BaseModel


# -------------------------------
# Owner Information
# -------------------------------

class PostOwner(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


# -------------------------------
# Create Post
# -------------------------------

class PostCreate(BaseModel):
    title: str
    content: str


# -------------------------------
# Post Response
# -------------------------------

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    user_id: int

    class Config:
        from_attributes = True


# -------------------------------
# Post With Owner
# -------------------------------

class PostWithOwner(BaseModel):
    id: int
    title: str
    content: str

    owner: PostOwner

    class Config:
        from_attributes = True