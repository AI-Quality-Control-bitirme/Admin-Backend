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

## Roller ve şirket kaydı

| Rol | Değer | Şirket |
| --- | --- | --- |
| Super Admin | `super_admin` | Yok, platformun tamamını yönetir |
| Company Admin | `company_admin` | Kendi şirketi |
| HR | `hr` | Kendi şirketi |
| Operator | `operator` | Kendi şirketi |

`POST /companies/register` şirketi ve ilk Company Admin hesabını tek işlemde oluşturur. İstek gövdesi: `company_name`, `admin_full_name`, `admin_email`, `admin_password` (en az 8 karakter). Şirket adı (büyük/küçük harf farkı gözetmeden) ya da e-posta zaten kayıtlıysa `409` döner. Parolalar bcrypt ile saklanır ve hiçbir yanıtta dönmez.

## Super Admin hesabı

Super Admin API üzerinden oluşturulamaz. Sunucuda bir kez şu komutla oluşturulur:

```sh
python -m app.cli.create_super_admin --email admin@ornek.com --full-name "Platform Yöneticisi"
```

Parola gizli olarak iki kez sorulur ya da `SUPER_ADMIN_PASSWORD` ortam değişkeninden okunur, böylece komut geçmişinde görünmez. Veritabanı yalnızca bir Super Admin'e izin verir; ikinci denemede komut hata verir.

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
