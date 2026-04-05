from datetime import timedelta
from http import HTTPStatus
from unittest.mock import patch

from app.core.security import (
    create_access_token,
    get_password_hash,
    verify_password,
)


def test_get_password_hash_returns_hashed_string(faker):
    password = faker.password()
    hashed = get_password_hash(password)

    assert hashed != password
    assert isinstance(hashed, str)


def test_verify_password_returns_true_for_correct_password(faker):
    password = faker.password()
    hashed = get_password_hash(password)

    assert verify_password(password, hashed) is True


def test_verify_password_returns_false_for_wrong_password(faker):
    hashed = get_password_hash(faker.password())

    assert verify_password('wrong-password', hashed) is False


def test_create_access_token_returns_string(faker):
    token = create_access_token(data={'sub': faker.email()})

    assert isinstance(token, str)
    assert len(token) > 0


def test_jwt_invalid_token_returns_401(client, user):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': 'Bearer token-invalido'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_expired_token_returns_401(client, user):
    with patch('app.core.security.timedelta') as mock_td:
        mock_td.return_value = timedelta(minutes=-1)
        expired_token = create_access_token(data={'sub': user.email})

    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {expired_token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_token_without_sub_returns_401(client, user):
    token = create_access_token(data={})

    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_jwt_token_with_nonexistent_user_returns_401(client):
    token = create_access_token(data={'sub': 'ghost@email.com'})

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
