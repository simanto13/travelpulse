.PHONY: run test lint docker-build

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -q

docker-build:
	docker-compose build
