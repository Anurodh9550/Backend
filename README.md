# Message Chair Backend (DRF + PostgreSQL + Redis + Realtime)

Ye backend Django REST Framework par bana hai aur production-ready stack follow karta hai:
- API data ke liye PostgreSQL
- Cache + realtime channels ke liye Redis
- Realtime WebSocket support ke liye Django Channels

## 1) Local infra start karo (Postgres + Redis)

```bash
docker compose up -d
```

## 2) Python setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 3) Environment setup

```bash
copy .env.example .env
```

`.env` me by default `DB_ENGINE=postgres` diya hua hai.

## 4) DB migrate + sample data

```bash
python manage.py migrate
python manage.py loaddata catalog/fixtures/sample_data.json
```

## 5) Run backend

```bash
python manage.py runserver
```

## API Endpoints

- `GET /health/` - health check
- `GET /api/collections/`
- `POST /api/collections/` (admin key required)
- `GET /api/products/`
- `GET /api/products/?collection=opulent-prime`
- `POST /api/products/` (admin key required)
- `PUT/PATCH/DELETE /api/products/{id}/` (admin key required)

### Admin API Key Security

Industry-style basic hardening ke liye admin routes par API key protection enabled hai.

1. `.env` me `ADMIN_API_KEY=your-strong-key` set karo.
2. Admin panel requests me header bhejo:

```http
X-Admin-Api-Key: your-strong-key
```

Protected endpoints:
- `/api/admin-stats/`
- non-public CRUD on contact/warranty/support
- collection/product create/update/delete

## Realtime WebSocket

- `ws://127.0.0.1:8000/ws/health/`
- Connection hote hi welcome message aata hai
- Jo text bhejoge, server echo karke return karega

## Admin Panel

```bash
python manage.py createsuperuser
```

Open: `http://127.0.0.1:8000/admin/`
