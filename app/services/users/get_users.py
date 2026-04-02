from typing import List

from sqlalchemy.orm import Session

from app.models import User
from app.repositories import get_users


def get_users_service(
    session: Session, skip: int = 0, limit: int = 100
) -> List[User]:
    return get_users(session, skip, limit)
