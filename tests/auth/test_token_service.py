from http import HTTPStatus

import pytest
from fastapi import HTTPException

from app.services.auth.token import login_for_access_token_service


def test_login_returns_access_token(session, user):
    result = login_for_access_token_service(
        email=user.email,
        password=user.clean_password,
        session=session,
    )

    assert 'access_token' in result
    assert result['token_type'] == 'bearer'
    assert isinstance(result['access_token'], str)


def test_login_raises_401_when_user_not_found(session, faker):
    with pytest.raises(HTTPException) as exc:
        login_for_access_token_service(
            email=faker.email(),
            password=faker.password(),
            session=session,
        )

    assert exc.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exc.value.detail == 'Incorrect email or password'


def test_login_raises_401_when_password_is_wrong(session, user, faker):
    with pytest.raises(HTTPException) as exc:
        login_for_access_token_service(
            email=user.email,
            password='wrong-password',
            session=session,
        )

    assert exc.value.status_code == HTTPStatus.UNAUTHORIZED
    assert exc.value.detail == 'Incorrect email or password'
