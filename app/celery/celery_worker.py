from celery import Celery

celery = Celery(
    "backend_foundation",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0",
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