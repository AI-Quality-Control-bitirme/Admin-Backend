from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.models import Company, User, UserRole


def registration(**overrides: Any) -> dict[str, Any]:
    body = {
        "company_name": "Rezona Otel",
        "admin_full_name": "Ayşe Yılmaz",
        "admin_email": "Ayse@Rezona.example",
        "admin_password": "guclu-parola-1",
    }
    body.update(overrides)
    return body


def test_registration_creates_company_and_admin(client: TestClient, db_session: Session) -> None:
    response = client.post("/companies/register", json=registration())

    assert response.status_code == 201
    body = response.json()
    assert body["company"]["name"] == "Rezona Otel"
    admin = body["admin"]
    assert admin["email"] == "ayse@rezona.example"
    assert admin["full_name"] == "Ayşe Yılmaz"
    assert admin["role"] == "company_admin"
    assert admin["company_id"] == body["company"]["id"]
    assert admin["is_active"] is True
    assert "password" not in str(body)

    company = db_session.scalar(select(Company))
    user = db_session.scalar(select(User))
    assert company is not None and user is not None
    assert user.company_id == company.id
    assert user.role is UserRole.COMPANY_ADMIN
    assert user.password_hash != "guclu-parola-1"
    assert verify_password("guclu-parola-1", user.password_hash)


def test_duplicate_company_name_is_rejected_case_insensitively(client: TestClient) -> None:
    assert client.post("/companies/register", json=registration()).status_code == 201

    response = client.post(
        "/companies/register",
        json=registration(company_name="REZONA otel", admin_email="baska@rezona.example"),
    )

    assert response.status_code == 409


def test_duplicate_admin_email_is_rejected(client: TestClient, db_session: Session) -> None:
    assert client.post("/companies/register", json=registration()).status_code == 201

    response = client.post(
        "/companies/register",
        json=registration(company_name="Başka Otel", admin_email="AYSE@rezona.example"),
    )

    assert response.status_code == 409
    assert len(db_session.scalars(select(Company)).all()) == 1


@pytest.mark.parametrize(
    "overrides",
    [
        {"company_name": "   "},
        {"admin_full_name": ""},
        {"admin_email": "not-an-email"},
        {"admin_password": "short"},
        {"admin_password": "ş" * 40},
    ],
)
def test_invalid_registration_returns_422(client: TestClient, overrides: dict[str, Any]) -> None:
    response = client.post("/companies/register", json=registration(**overrides))

    assert response.status_code == 422


def test_registration_cannot_choose_role(client: TestClient) -> None:
    response = client.post("/companies/register", json=registration(role="super_admin"))

    assert response.status_code == 201
    assert response.json()["admin"]["role"] == "company_admin"


def test_all_four_roles_are_defined() -> None:
    assert {role.value for role in UserRole} == {"super_admin", "company_admin", "hr", "operator"}
