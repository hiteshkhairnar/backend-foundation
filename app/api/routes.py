from fastapi import APIRouter

from app.api.users import router as users_router
from app.api.posts import router as posts_router
from app.api.comments import router as comments_router
from app.api.likes import router as likes_router
from app.api.bookmarks import router as bookmarks_router


router = APIRouter()

router.include_router(users_router)
router.include_router(posts_router)
router.include_router(comments_router)
router.include_router(likes_router)
router.include_router(bookmarks_router)


@router.get("/")
def home():
    return {
        "message": "Mission Global Engineer 🚀"
    }


@router.get("/about")
def about():
    return {
        "developer": "Hitesh Khairnar",
        "goal": "Backend Developer + AI Engineer"
    }