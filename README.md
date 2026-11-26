# Admin Service

Şirket, kullanıcı ve rol yönetimini sağlayan FastAPI servisi. Veriler PostgreSQL'de tutulur, şema Alembic ile yönetilir.

## Çalıştırma

Python 3.12 ve Docker ile proje klasöründe:

```sh
python -m venv .venv
.venv\Scripts\activate            # macOS/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
copy .env.example .env            # macOS/Linux: cp .env.example .env
docker compose up -d db
alembic upgrade head
uvicorn app.main:app --reload --port 8001
```

`GET /health` veritabanına `SELECT 1` gönderir. Bağlantı varsa `200 {"status": "ok", "database": "ok"}`, yoksa `503` döner. API belgeleri `http://localhost:8001/docs` adresindedir.

## Testler

```sh
pytest
```

Testler bellek içi SQLite kullanır, PostgreSQL gerektirmez.

## Yeni migration

```sh
alembic revision --autogenerate -m "açıklama"
alembic upgrade head
```
