from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.enums import UserRole
from app.models.user import User
from app.repositories.company_repository import CompanyRepository
from app.repositories.user_repository import UserRepository
from app.schemas.company import CompanyRegister
from app.services.errors import ConflictError


class RegistrationService:
    def __init__(self, session: Session) -> None:
        self._session = session
        self._companies = CompanyRepository(session)
        self._users = UserRepository(session)

    def register_company(self, data: CompanyRegister) -> tuple[Company, User]:
        if self._companies.name_exists(data.company_name):
            raise ConflictError("A company with this name is already registered")
        if self._users.email_exists(data.admin_email):
            raise ConflictError("This e-mail address is already in use")

        try:
            company = self._companies.add(data.company_name)
            admin = self._users.add(
                email=data.admin_email,
                full_name=data.admin_full_name,
                password=data.admin_password,
                role=UserRole.COMPANY_ADMIN,
                company_id=company.id,
            )
            self._session.commit()
        except IntegrityError as exc:
            self._session.rollback()
            raise ConflictError("Company name or e-mail address is already in use") from exc

        self._session.refresh(company)
        self._session.refresh(admin)
        return company, admin

    def create_super_admin(self, *, email: str, full_name: str, password: str) -> User:
        if self._users.super_admin_exists():
            raise ConflictError("A Super Admin account already exists")
        if self._users.email_exists(email):
            raise ConflictError("This e-mail address is already in use")

        user = self._users.add(
            email=email,
            full_name=full_name,
            password=password,
            role=UserRole.SUPER_ADMIN,
            company_id=None,
        )
        self._session.commit()
        self._session.refresh(user)
        return user
