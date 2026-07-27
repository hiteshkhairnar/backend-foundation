import time

from app.celery.celery_worker import celery


@celery.task(name="send_email")
def send_email(email: str):

    print("=" * 50)
    print(f"Sending email to {email}")

    time.sleep(5)

    print(f"Email sent successfully to {email}")
    print("=" * 50)

    return "Success"