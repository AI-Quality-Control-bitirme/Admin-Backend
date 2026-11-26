from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.company import Company


class CompanyRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def name_exists(self, name: str) -> bool:
        stmt = select(Company.id).where(func.lower(Company.name) == name.lower())
        return self._session.scalar(stmt) is not None

    def add(self, name: str) -> Company:
        company = Company(name=name)
        self._session.add(company)
        self._session.flush()
        return company
