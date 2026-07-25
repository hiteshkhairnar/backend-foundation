from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.base import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)

    content = Column(String, nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    post_id = Column(
        Integer,
        ForeignKey("posts.id")
    )

    owner = relationship(
        "User",
        back_populates="comments"
    )

    post = relationship(
        "Post",
        back_populates="comments"
    )