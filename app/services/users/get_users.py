from typing import List

from sqlalchemy.orm import Session

from app.models import User
from app.repositories import get_users
from app.schemas import FilterPage


def get_users_service(session: Session, filter_page: FilterPage) -> List[User]:
    return get_users(session, filter_page.offset, filter_page.limit)
