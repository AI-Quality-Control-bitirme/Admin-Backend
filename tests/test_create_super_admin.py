import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.cli.create_super_admin import main
from app.core.security import verify_password
from app.models import Company, User, UserRole

ARGS = ["--email", "Root@Platform.example", "--full-name", "Platform Admin"]


def run(db_session: Session, args: list[str] = ARGS, password: str = "cok-guclu-parola") -> int:
    return main(args, session_factory=lambda: db_session, read_password=lambda: password)


def test_creates_super_admin_without_company(db_session: Session) -> None:
    assert run(db_session) == 0

    user = db_session.scalar(select(User))
    assert user is not None
    assert user.role is UserRole.SUPER_ADMIN
    assert user.company_id is None
    assert user.email == "root@platform.example"
    assert verify_password("cok-guclu-parola", user.password_hash)


def test_second_super_admin_is_refused(db_session: Session) -> None:
    assert run(db_session) == 0

    assert run(db_session, ["--email", "other@platform.example", "--full-name", "Other"]) == 1
    assert len(db_session.scalars(select(User)).all()) == 1


def test_weak_password_is_refused(db_session: Session) -> None:
    assert run(db_session, password="kisa") == 2
    assert db_session.scalar(select(User)) is None


def test_database_allows_only_one_super_admin(db_session: Session) -> None:
    db_session.add_all(
        [
            User(email=f"root{i}@platform.example", full_name="Root", password_hash="x",
                 role=UserRole.SUPER_ADMIN, company_id=None)
            for i in range(2)
        ]
    )
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_database_rejects_company_user_without_company(db_session: Session) -> None:
    db_session.add(User(email="hr@x.example", full_name="HR", password_hash="x",
                        role=UserRole.HR, company_id=None))
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_database_rejects_super_admin_with_company(db_session: Session) -> None:
    company = Company(name="Rezona")
    db_session.add(company)
    db_session.flush()
    db_session.add(User(email="root@x.example", full_name="Root", password_hash="x",
                        role=UserRole.SUPER_ADMIN, company_id=company.id))
    with pytest.raises(IntegrityError):
        db_session.commit()
