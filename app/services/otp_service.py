from app.database.redis import redis_client
from app.utils.otp import generate_otp


def create_otp(email: str):
    otp = generate_otp()

    redis_client.set(
        f"otp:{email}",
        otp,
        ex=300,   # expires in 5 minutes
    )

    return otp


def verify_otp(email: str, otp: str):
    stored_otp = redis_client.get(f"otp:{email}")

    if stored_otp is None:
        return False

    return stored_otp == otp