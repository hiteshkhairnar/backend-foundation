from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.utils.hashing import hash_password, verify_password
from app.auth.jwt_handler import create_access_token
from sqlalchemy import or_, desc

def create_user(db: Session, user: UserCreate):
    db_user = User(
    name=user.name,
    email=user.email,
    hashed_password=hash_password(user.password),
    role="user"
)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def get_users(
    db: Session,
    page: int = 1,
    limit: int = 10,
    search: str = "",
    sort: str = "latest"
):
    query = db.query(User)

    if search:
        query = query.filter(
            or_(
                User.name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
        )

    if sort == "name":
        query = query.order_by(User.name)

    elif sort == "email":
        query = query.order_by(User.email)

    elif sort == "oldest":
        query = query.order_by(User.id)

    else:
        query = query.order_by(desc(User.id))

    total = query.count()

    users = (
        query.offset((page - 1) * limit)
             .limit(limit)
             .all()
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "users": users
    }


def update_user(db: Session, user_id: int, user: UserCreate):
    db_user = get_users(db, user_id)

    if not db_user:
        return None

    db_user.name = user.name
    db_user.email = user.email

    db.commit()
    db.refresh(db_user)

    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_users(db, user_id)

    if not db_user:
        return None

    db.delete(db_user)
    db.commit()

    return db_user

def login_user(db: Session, user: UserLogin):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        return None

    if not verify_password(user.password, db_user.hashed_password):
        return None

    access_token = create_access_token(
        {"sub": db_user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }