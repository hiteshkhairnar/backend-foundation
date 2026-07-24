from pydantic import BaseModel, EmailStr

# ---------------------------------------------------
# Post Schema (Nested)
# ---------------------------------------------------

class PostInUser(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True


# ---------------------------------------------------
# User Schemas
# ---------------------------------------------------

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    profile_image: str | None = None

    class Config:
        from_attributes = True


# ---------------------------------------------------
# User with Posts
# ---------------------------------------------------

class UserWithPosts(UserResponse):
    posts: list[PostInUser] = []

    class Config:
        from_attributes = True