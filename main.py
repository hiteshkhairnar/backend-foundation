from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router as main_router
from app.api.users import router as users_router

app = FastAPI(
    title="Backend Foundation",
    version="1.0.0"
)

# Mount uploads folder
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include routers
app.include_router(main_router)
app.include_router(users_router)