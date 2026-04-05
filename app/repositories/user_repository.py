from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserRequest


def get_user_by_username_or_email(
    session: Session, username: str, email: str
) -> User | None:
    return session.scalar(
        select(User).where((User.username == username) | (User.email == email))
    )


def get_user_by_id(session: Session, user_id: int) -> User | None:
    return session.scalar(select(User).where(User.id == user_id))


def get_user_by_email(session: Session, email: str) -> User | None:
    return session.scalar(select(User).where(User.email == email))


def get_users(session: Session, skip: int = 0, limit: int = 100) -> List[User]:
    return session.scalars(select(User).offset(skip).limit(limit)).all()


def create_user(session: Session, user: UserRequest) -> User:
    db_user = User(
        username=user.username, password=user.password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def update_user(session: Session, db_user: User, user: UserRequest) -> User:
    db_user.username = user.username
    db_user.password = user.password
    db_user.email = user.email
    session.commit()
    session.refresh(db_user)
    return db_user


def delete_user(session: Session, db_user: User) -> None:
    session.delete(db_user)
    session.commit()
