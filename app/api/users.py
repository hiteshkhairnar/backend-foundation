from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.user import UserLogin
from app.auth.dependencies import get_current_user
from app.models.user import User
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserResponse
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.auth.admin import admin_required

from app.database.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services import user_service
from app.services.user_service import (
    create_user,
    get_users,
    update_user,
    delete_user,
    login_user,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse)
def create_new_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    new_user = create_user(db, user)

    if not new_user:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    return new_user
@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = UserLogin(
        email=form_data.username,
        password=form_data.password
    )

    token = login_user(db, user)

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return token



@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return get_users(db)


@router.put("/{user_id}", response_model=UserResponse)
def update_existing_user(
    user_id: int,
    user: UserCreate,
    db: Session = Depends(get_db)
):
    updated_user = update_user(db, user_id, user)

    if not updated_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return updated_user


@router.delete("/{user_id}")
def delete_existing_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    deleted_user = delete_user(db, user_id)

    if not deleted_user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully"
    }
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/admin")
def admin_dashboard(current_user=Depends(admin_required)):
    return {
        "message": "Welcome Admin!",
        "user": current_user.email
    }