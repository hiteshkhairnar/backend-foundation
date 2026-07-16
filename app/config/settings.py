from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("postgresql://postgres:postgres123@localhost:5432/backend_foundation")
SECRET_KEY = os.getenv("9f9c4917b3cfcf47dfaefbb4ef63466d12b32065fb03c7e317147547378a80e8")
ALGORITHM = os.getenv("HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("30")
)