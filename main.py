from fastapi import FastAPI
from app.api.routes import router as main_router
from app.api.users import router as users_router

app = FastAPI(
    title="Backend Foundation",
    version="1.0.0"
)

app.include_router(main_router)     # ✅ Correct
app.include_router(users_router)    # ✅ Correct