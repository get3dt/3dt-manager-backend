from http import HTTPStatus
from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.security import get_current_user
from app.db.database import get_session
from app.models import User
from app.schemas import FilterPage, UserRequest, UserResponse
from app.schemas.user_schema import Message
from app.services import (
    create_user_service,
    delete_user_service,
    get_users_service,
    update_user_service,
)

router = APIRouter(prefix='/users', tags=['users'])

Session = Annotated[Session, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserResponse)
def create_user(user: UserRequest, session: Session):
    return create_user_service(user, session)


@router.get('/', response_model=List[UserResponse])
def get_users(
    session: Session,
    filter_users: Annotated[FilterPage, Query()],
):
    return get_users_service(session, filter_users)


@router.put('/{user_id}', response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserRequest,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )

    return update_user_service(user_id, user, session)


@router.delete('/{user_id}', response_model=Message)
def delete_user(
    user_id: int,
    session: Session,
    current_user: CurrentUser,
):
    if current_user.id != user_id:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN, detail='Not enough permissions'
        )
    return delete_user_service(user_id, session)
