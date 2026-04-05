from http import HTTPStatus

from app.models import User


def test_create_user_returns_201(client, faker):
    response = client.post(
        '/users/',
        json={
            'username': faker.user_name(),
            'email': faker.email(),
            'password': faker.password(),
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    body = response.json()
    assert 'id' in body
    assert 'password' not in body


def test_create_user_returns_409_on_duplicate_username(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'other@email.com',
            'password': 'anypassword',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'Username already exists'


def test_create_user_returns_409_on_duplicate_email(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'otherusername',
            'email': user.email,
            'password': 'anypassword',
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'Email already exists'


def test_create_user_returns_422_on_invalid_email(client, faker):
    response = client.post(
        '/users/',
        json={
            'username': faker.user_name(),
            'email': 'not-an-email',
            'password': faker.password(),
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_users_returns_200_and_list(client, user):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    body = response.json()
    assert isinstance(body, list)
    assert len(body) == 1
    assert body[0]['id'] == user.id


def test_get_users_returns_empty_list_when_no_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == []


def test_get_users_respects_limit(client, faker, session):
    for _ in range(5):
        session.add(
            User(
                username=faker.user_name(),
                email=faker.email(),
                password=faker.password(),
            )
        )
    session.commit()

    response = client.get('/users/?limit=2')

    assert response.status_code == HTTPStatus.OK
    assert len(response.json()) == 2


def test_update_user_returns_200_with_updated_data(client, user, token, faker):
    new_username = faker.user_name()
    new_email = faker.email()

    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': new_username,
            'email': new_email,
            'password': faker.password(),
        },
    )

    assert response.status_code == HTTPStatus.OK
    body = response.json()
    assert body['id'] == user.id
    assert body['username'] == new_username
    assert body['email'] == new_email


def test_update_user_returns_401_without_token(client, user, faker):
    response = client.put(
        f'/users/{user.id}',
        json={
            'username': faker.user_name(),
            'email': faker.email(),
            'password': faker.password(),
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_update_user_returns_403_when_updating_another_user(
    client, user, token, faker
):
    second = client.post(
        '/users/',
        json={
            'username': faker.user_name(),
            'email': faker.email(),
            'password': faker.password(),
        },
    )
    second_id = second.json()['id']

    response = client.put(
        f'/users/{second_id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': faker.user_name(),
            'email': faker.email(),
            'password': faker.password(),
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()['detail'] == 'Not enough permissions'


def test_update_user_returns_409_on_duplicate_data(client, user, faker):
    second_password = faker.password()
    second_email = faker.email()
    second = client.post(
        '/users/',
        json={
            'username': faker.user_name(),
            'email': second_email,
            'password': second_password,
        },
    )
    second_id = second.json()['id']

    second_token = client.post(
        '/auth/token',
        data={
            'username': second_email,
            'password': second_password,
        },
    ).json()['access_token']

    response = client.put(
        f'/users/{second_id}',
        headers={'Authorization': f'Bearer {second_token}'},
        json={
            'username': user.username,
            'email': user.email,
            'password': faker.password(),
        },
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == 'Username or Email already exists'


def test_delete_user_returns_200_with_message(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_returns_401_without_token(client, user):
    response = client.delete(f'/users/{user.id}')

    assert response.status_code == HTTPStatus.UNAUTHORIZED


def test_delete_user_returns_403_when_deleting_another_user(
    client, user, token, faker
):
    second = client.post(
        '/users/',
        json={
            'username': faker.user_name(),
            'email': faker.email(),
            'password': faker.password(),
        },
    )
    second_id = second.json()['id']

    response = client.delete(
        f'/users/{second_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json()['detail'] == 'Not enough permissions'
