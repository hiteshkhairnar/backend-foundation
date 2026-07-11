from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["Users"])

class User(BaseModel):
    name: str
    email: str

users = []

@router.get("/")
def get_users():
    return users

@router.post("/")
def create_user(user: User):
    users.append(user)
    return {
        "message": "User created successfully",
        "user": user
    }

@router.get("/{user_id}")
def get_user(user_id: int):
    if user_id >= len(users):
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]