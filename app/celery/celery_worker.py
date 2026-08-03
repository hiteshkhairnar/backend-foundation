import os

from celery import Celery


REDIS_URL = os.getenv(
    "REDIS_URL",
    "redis://redis:6379/0",
)


celery = Celery(
    "backend_foundation",
    broker=REDIS_URL,
    backend=REDIS_URL,
)


celery.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)


# Import all task modules
celery.autodiscover_tasks(["app.tasks"])

# Explicit import (recommended)
import app.tasks.email_tasks