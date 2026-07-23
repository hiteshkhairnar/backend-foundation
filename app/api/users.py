from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.services.user_service import (
    create_user,
    get_users,
    update_user,
    delete_user,
    login_user,
)

from app.auth.dependencies import get_current_user
from app.auth.admin import admin_required
from app.services.upload_service import save_profile_image

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# Create User
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


# Login
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


# Get All Users (Pagination + Search + Sorting)
@router.get("/")
def read_users(
    page: int = 1,
    limit: int = 10,
    search: str = "",
    sort: str = "latest",
    db: Session = Depends(get_db)
):
    data = get_users(db, page, limit, search, sort)

    return {
        "success": True,
        "message": "Users fetched successfully",
        "data": {
            "total": data["total"],
            "page": data["page"],
            "limit": data["limit"],
            "users": [
                UserResponse.model_validate(user)
                for user in data["users"]
            ]
        }
    }


# Update User
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


# Delete User
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
        "success": True,
        "message": "User deleted successfully"
    }


# Current Logged-in User
@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user


# Admin Route
@router.get("/admin")
def admin_dashboard(
    current_user=Depends(admin_required)
):
    return {
        "success": True,
        "message": "Welcome Admin!",
        "user": current_user.email
    }


# Upload Profile Image
@router.post("/upload-profile-image")
def upload_profile_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    image_path = save_profile_image(file)

    current_user.profile_image = image_path

    db.commit()
    db.refresh(current_user)

    return {
        "success": True,
        "message": "Profile image uploaded successfully",
        "image_url": image_path,
    }