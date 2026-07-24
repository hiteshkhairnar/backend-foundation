from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import RequestValidationError

import time
import logging

from app.api.routes import router as main_router
from app.api.users import router as users_router
from app.api.posts import router as posts_router

from app.exceptions.handlers import (
    validation_exception_handler,
    generic_exception_handler,
)

# ----------------------------------------------------
# Logging Configuration
# ----------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# ----------------------------------------------------
# FastAPI App
# ----------------------------------------------------

app = FastAPI(
    title="Backend Foundation",
    version="1.0.0"
)

# ----------------------------------------------------
# Logging Middleware
# ----------------------------------------------------

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = time.time() - start_time

    logger.info(
        f"{request.method} {request.url.path} | "
        f"Status: {response.status_code} | "
        f"Time: {process_time:.4f}s"
    )

    response.headers["X-Process-Time"] = str(process_time)

    return response

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
# Routers
# ----------------------------------------------------

app.include_router(main_router)
app.include_router(users_router)
app.include_router(posts_router)

# ----------------------------------------------------
# Static Files
# ----------------------------------------------------

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads",
)