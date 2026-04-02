from http import HTTPStatus

import pytest
from fastapi import HTTPException

from app.schemas import UserRequest
from app.services.users.create_user import create_user_service
from app.services.users.delete_user import delete_user_service
from app.services.users.get_users import get_users_service
from app.services.users.update_user import update_user_service


def test_create_user_service_returns_created_user(session, faker):
    user_data = UserRequest(
        username=faker.user_name(),
        email=faker.email(),
        password=faker.password(),
    )

    result = create_user_service(user_data, session)

    assert result.id is not None
    assert result.username == user_data.username
    assert result.email == user_data.email


def test_create_user_service_raises_conflict_on_duplicate_username(
    session, user
):
    duplicate = UserRequest(
        username=user.username,
        email='other@email.com',
        password='anypassword',
    )

    with pytest.raises(HTTPException) as exc:
        create_user_service(duplicate, session)

    assert exc.value.status_code == HTTPStatus.CONFLICT
    assert exc.value.detail == 'Username already exists'


def test_create_user_service_raises_conflict_on_duplicate_email(session, user):
    duplicate = UserRequest(
        username='otherusername',
        email=user.email,
        password='anypassword',
    )

    with pytest.raises(HTTPException) as exc:
        create_user_service(duplicate, session)

    assert exc.value.status_code == HTTPStatus.CONFLICT
    assert exc.value.detail == 'Email already exists'


def test_get_users_service_returns_list(session, user):
    result = get_users_service(session)

    assert isinstance(result, list)
    assert len(result) == 1


def test_get_users_service_returns_empty_list_when_no_users(session):
    result = get_users_service(session)

    assert result == []


def test_update_user_service_returns_updated_user(session, user, faker):
    user_data = UserRequest(
        username=faker.user_name(),
        email=faker.email(),
        password=faker.password(),
    )

    result = update_user_service(user.id, user_data, session)

    assert result.username == user_data.username
    assert result.email == user_data.email


def test_update_user_service_raises_not_found(session, faker):
    user_data = UserRequest(
        username=faker.user_name(),
        email=faker.email(),
        password=faker.password(),
    )

    with pytest.raises(HTTPException) as exc:
        update_user_service(999, user_data, session)

    assert exc.value.status_code == HTTPStatus.NOT_FOUND
    assert exc.value.detail == 'User not found'


def test_update_user_service_raises_conflict_on_duplicate_data(
    session, user, faker
):
    second_user = UserRequest(
        username=faker.user_name(),
        email=faker.email(),
        password=faker.password(),
    )
    second = create_user_service(second_user, session)

    with pytest.raises(HTTPException) as exc:
        update_user_service(
            second.id,
            UserRequest(
                username=user.username,
                email=user.email,
                password=faker.password(),
            ),
            session,
        )

    assert exc.value.status_code == HTTPStatus.CONFLICT
    assert exc.value.detail == 'Username or Email already exists'


def test_delete_user_service_returns_message(session, user):
    result = delete_user_service(user.id, session)

    assert result == {'message': 'User deleted'}


def test_delete_user_service_raises_not_found(session):
    with pytest.raises(HTTPException) as exc:
        delete_user_service(999, session)

    assert exc.value.status_code == HTTPStatus.NOT_FOUND
    assert exc.value.detail == 'User not found'
