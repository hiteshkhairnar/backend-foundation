import os
import uuid
from fastapi import UploadFile, HTTPException

UPLOAD_DIR = "uploads/profiles"

ALLOWED_TYPES = {
    "image/jpeg",
    "image/png",
    "image/jpg"
}

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2 MB


def save_profile_image(file: UploadFile):
    # Validate content type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail="Only JPG, JPEG and PNG files are allowed."
        )

    # Read file
    content = file.file.read()

    # Validate size
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 2 MB."
        )

    # Create uploads directory if it doesn't exist
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Generate unique filename
    extension = os.path.splitext(file.filename)[1]
    filename = f"{uuid.uuid4()}{extension}"

    filepath = os.path.join(UPLOAD_DIR, filename)

    # Save file
    with open(filepath, "wb") as f:
        f.write(content)

    return filepath