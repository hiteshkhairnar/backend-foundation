from fastapi import APIRouter

from app.celery.tasks import send_email

router = APIRouter(
    prefix="/celery",
    tags=["Celery"],
)


@router.get("/send-email")
def send_test_email():

    send_email.delay("hitesh@example.com")

    return {
        "message": "Email task added to queue"
    }