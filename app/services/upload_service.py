import os
import shutil
import uuid

from fastapi import UploadFile, HTTPException


UPLOAD_FOLDER = "uploads"

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".webp",
}


def save_profile_image(file: UploadFile):

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only image files are allowed.",
        )

    filename = f"{uuid.uuid4()}{extension}"

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True,
    )

    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename,
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer,
        )

    return file_path