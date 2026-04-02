from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import User
from app.repositories import create_user, get_user_by_username_or_email
from app.schemas import UserRequest


def create_user_service(user: UserRequest, session: Session) -> User:
    db_user = get_user_by_username_or_email(session, user.username, user.email)

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email already exists',
            )

    return create_user(session, user)
