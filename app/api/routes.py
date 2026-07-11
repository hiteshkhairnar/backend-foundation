from fastapi import APIRouter

router = APIRouter()

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