from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.repositories import get_user_by_email
from app.schemas import Token


def login_for_access_token_service(
    email: str, password: str, session: Session
) -> Token:
    user = get_user_by_email(session, email)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    if not verify_password(password=password, hashed_password=user.password):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': user.email})

    return {'access_token': access_token, 'token_type': 'bearer'}
