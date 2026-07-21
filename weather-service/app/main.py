from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.logging import configure_logging

configure_logging()

app = FastAPI(title="SkySense - Weather Service", version="0.1.0")

app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def on_startup():
    # place for startup tasks: db, cache, kafka clients
    app.state.settings = settings


@app.on_event("shutdown")
async def on_shutdown():
    # clean up clients, connections
    pass
