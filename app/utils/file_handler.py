import os
import shutil
from uuid import uuid4

from fastapi import UploadFile


UPLOAD_DIR = "uploads"


def save_image(file: UploadFile):

    # Allowed image types
    allowed_extensions = [
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".webp",
    ]

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in allowed_extensions:
        raise ValueError("Only image files are allowed.")

    filename = f"{uuid4()}{extension}"

    file_path = os.path.join(
        UPLOAD_DIR,
        filename,
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return file_path