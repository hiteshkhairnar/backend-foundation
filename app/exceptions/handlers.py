from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.utils.logger import logger


# -----------------------------------------
# Validation Error
# -----------------------------------------

async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    logger.error(
        f"Validation Error | {request.url.path} | {exc.errors()}"
    )

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation Error",
            "errors": exc.errors(),
        },
    )


# -----------------------------------------
# Generic Exception
# -----------------------------------------

async def generic_exception_handler(
    request: Request,
    exc: Exception,
):
    logger.exception(
        f"Unhandled Exception | {request.url.path}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error",
        },
    )