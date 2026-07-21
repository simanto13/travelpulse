# SkySense — Weather Service

FastAPI microservice scaffold for SkySense.

Quickstart (local):
1. Create a virtualenv and install deps:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements/production.txt
2. Run:
   uvicorn app.main:app --reload --port 8000

API:
- GET /api/v1/health
- GET /api/v1/weather/current?city={city}
- POST /api/v1/weather/report

Docker:
- docker-compose up --build

Testing:
- make test
