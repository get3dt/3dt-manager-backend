from http import HTTPStatus
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_session
from app.schemas import UserRequest, UserResponse
from app.schemas.user_schema import Message
from app.services import (
    create_user_service,
    delete_user_service,
    get_users_service,
    update_user_service,
)

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/', status_code=HTTPStatus.CREATED, response_model=UserResponse)
def create_user(user: UserRequest, session: Session = Depends(get_session)):
    return create_user_service(user, session)


@router.get('/', response_model=List[UserResponse])
def get_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    return get_users_service(session, skip, limit)


@router.put('/{user_id}', response_model=UserResponse)
def update_user(
    user_id: int, user: UserRequest, session: Session = Depends(get_session)
):
    return update_user_service(user_id, user, session)


@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    return delete_user_service(user_id, session)
