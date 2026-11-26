from unittest.mock import MagicMock

from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app.db.session import get_db
from app.main import app


def test_health_reports_database_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


def test_health_returns_503_when_database_is_down() -> None:
    broken = MagicMock()
    broken.execute.side_effect = OperationalError("SELECT 1", {}, Exception("down"))
    app.dependency_overrides[get_db] = lambda: broken
    try:
        with TestClient(app) as test_client:
            response = test_client.get("/health")
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json() == {"status": "error", "database": "unavailable"}
