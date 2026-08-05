from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

from app.middleware.logging_middleware import LoggingMiddleware

from app.api.routes import router as main_router
from app.api.users import router as users_router
from app.api.posts import router as posts_router
from app.api.comments import router as comments_router
from app.api.likes import router as likes_router
from app.api.bookmarks import router as bookmarks_router
from app.api.celery import router as celery_router

# Import models so SQLAlchemy registers them
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like
from app.models.bookmark import Bookmark

from app.exceptions.handlers import (
    validation_exception_handler,
    generic_exception_handler,
)

# ----------------------------------------------------
# FastAPI App
# ----------------------------------------------------

app = FastAPI(
    title="Backend Foundation",
    version="1.0.0",
)

# ----------------------------------------------------
# Middleware
# ----------------------------------------------------

app.add_middleware(LoggingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------
# Exception Handlers
# ----------------------------------------------------

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)

app.add_exception_handler(
    Exception,
    generic_exception_handler,
)

# ----------------------------------------------------
# Static Files
# ----------------------------------------------------

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads",
)

# ----------------------------------------------------
# Health Check
# ----------------------------------------------------

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "Backend Foundation",
        "version": "1.0.0",
    }

# ----------------------------------------------------
# Routers
# ----------------------------------------------------

app.include_router(main_router)
app.include_router(celery_router)