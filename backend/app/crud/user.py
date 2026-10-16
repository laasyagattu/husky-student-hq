from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.scalar(select(User).where(User.email == email.lower()))


def create_user(db: Session, data: UserCreate) -> User:
    user = User(email=data.email.lower(), hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user