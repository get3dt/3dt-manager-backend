from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import User
from app.repositories import get_user_by_id, update_user
from app.schemas import UserRequest


def update_user_service(
    user_id: int, user: UserRequest, session: Session
) -> User:
    db_user = get_user_by_id(session, user_id)

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    try:
        return update_user(session, db_user, user)
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username or Email already exists',
        )
