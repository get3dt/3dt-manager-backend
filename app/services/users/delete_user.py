from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories import delete_user, get_user_by_id
from app.schemas.user_schema import Message


def delete_user_service(user_id: int, session: Session) -> Message:
    db_user = get_user_by_id(session, user_id)

    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='User not found'
        )

    delete_user(session, db_user)
    return {'message': 'User deleted'}
