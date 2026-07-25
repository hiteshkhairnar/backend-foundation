from app.database.database import engine
from app.database.base import Base

# Import all models
from app.models.user import User
from app.models.post import Post
from app.models.comment import Comment
from app.models.like import Like
from app.models.bookmark import Bookmark


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("✅ Tables Created Successfully!")


if __name__ == "__main__":
    create_tables()