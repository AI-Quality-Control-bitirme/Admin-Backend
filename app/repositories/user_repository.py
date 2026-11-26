import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.enums import UserRole
from app.models.user import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email.lower())
        return self._session.scalar(stmt)

    def email_exists(self, email: str) -> bool:
        return self.get_by_email(email) is not None

    def super_admin_exists(self) -> bool:
        stmt = select(User.id).where(User.role == UserRole.SUPER_ADMIN)
        return self._session.scalar(stmt) is not None

    def add(
        self,
        *,
        email: str,
        full_name: str,
        password: str,
        role: UserRole,
        company_id: uuid.UUID | None,
    ) -> User:
        user = User(
            email=email.lower(),
            full_name=full_name,
            password_hash=hash_password(password),
            role=role,
            company_id=company_id,
        )
        self._session.add(user)
        self._session.flush()
        return user
