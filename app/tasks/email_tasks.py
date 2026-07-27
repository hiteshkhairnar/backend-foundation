from fastapi_mail import FastMail, MessageSchema, MessageType

from app.celery.celery_worker import celery
from app.config.mail_config import conf


@celery.task(name="send_otp_email")
def send_otp_email(email: str, otp: str):

    message = MessageSchema(
        subject="Your OTP Code",
        recipients=[email],
        body=f"""
Hello,

Your OTP is:

{otp}

It will expire in 5 minutes.

Backend Foundation
""",
        subtype=MessageType.plain,
    )

    fm = FastMail(conf)

    import asyncio
    asyncio.run(fm.send_message(message))

    return "Email Sent Successfully"