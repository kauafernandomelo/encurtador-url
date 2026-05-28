from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from url_shortener.api import router
from url_shortener.config import get_settings
from url_shortener.database import create_tables
from url_shortener.frontend import configure_frontend


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    create_tables()
    yield


def create_app(create_database: bool = True) -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        description=(
            "API REST para criar URLs curtas, redirecionar e consultar estatísticas."
        ),
        version="0.1.0",
        lifespan=lifespan if create_database else None,
    )
    configure_frontend(app)
    app.include_router(router)
    return app


app = create_app()
