from app.models import User
from app.repositories.user_repository import (
    create_user,
    delete_user,
    get_user_by_id,
    get_user_by_username_or_email,
    get_users,
    update_user,
)
from app.schemas import UserRequest


def test_get_user_by_id_returns_user(session, user):
    result = get_user_by_id(session, user.id)

    assert result is not None
    assert result.id == user.id


def test_get_user_by_id_returns_none_when_not_found(session):
    result = get_user_by_id(session, 999)

    assert result is None


def test_get_user_by_username_or_email_finds_by_username(session, user):
    result = get_user_by_username_or_email(
        session, user.username, 'other@email.com'
    )

    assert result is not None
    assert result.username == user.username


def test_get_user_by_username_or_email_finds_by_email(session, user):
    result = get_user_by_username_or_email(
        session, 'otherusername', user.email
    )

    assert result is not None
    assert result.email == user.email


def test_get_user_by_username_or_email_returns_none_when_not_found(session):
    result = get_user_by_username_or_email(session, 'ghost', 'ghost@email.com')

    assert result is None


def test_get_users_returns_all_users(session, faker):
    for _ in range(3):
        session.add(
            User(
                username=faker.user_name(),
                email=faker.email(),
                password=faker.password(),
            )
        )
    session.commit()

    result = get_users(session)

    assert len(result) == 3


def test_get_users_respects_limit(session, faker):
    for _ in range(5):
        session.add(
            User(
                username=faker.user_name(),
                email=faker.email(),
                password=faker.password(),
            )
        )
    session.commit()

    result = get_users(session, limit=2)

    assert len(result) == 2


def test_get_users_respects_skip(session, faker):
    for _ in range(3):
        session.add(
            User(
                username=faker.user_name(),
                email=faker.email(),
                password=faker.password(),
            )
        )
    session.commit()

    result = get_users(session, skip=2)

    assert len(result) == 1


def test_get_users_returns_empty_list_when_no_users(session):
    result = get_users(session)

    assert result == []


def test_create_user_persists_and_returns_with_id(session, faker):
    user_data = UserRequest(
        username=faker.user_name(),
        email=faker.email(),
        password=faker.password(),
    )

    result = create_user(session, user_data)

    assert result.id is not None
    assert result.username == user_data.username
    assert result.email == user_data.email


def test_update_user_persists_new_values(session, user, faker):
    user_data = UserRequest(
        username=faker.user_name(),
        email=faker.email(),
        password=faker.password(),
    )

    result = update_user(session, user, user_data)

    assert result.username == user_data.username
    assert result.email == user_data.email
    assert result.password == user_data.password


def test_delete_user_removes_from_database(session, user):
    delete_user(session, user)

    assert get_user_by_id(session, user.id) is None
