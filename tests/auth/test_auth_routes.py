from http import HTTPStatus


def test_get_token_returns_200_with_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token


def test_get_token_returns_401_when_user_not_found(client, faker):
    response = client.post(
        '/auth/token',
        data={'username': faker.email(), 'password': faker.password()},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Incorrect email or password'


def test_get_token_returns_401_when_password_is_wrong(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': 'wrong-password'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Incorrect email or password'
