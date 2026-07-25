from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    content = Column(String, nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    owner = relationship(
        "User",
        back_populates="posts",
    )

    comments = relationship(
    "Comment",
    back_populates="post",
    cascade="all, delete"
)
    likes = relationship(
    "Like",
    back_populates="post",
    cascade="all, delete"
)

    bookmarks = relationship(
    "Bookmark",
    back_populates="post",
    cascade="all, delete"
)