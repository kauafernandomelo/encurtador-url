from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

STATIC_DIR = Path(__file__).resolve().parent / "static"
INDEX_FILE = STATIC_DIR / "index.html"


def configure_frontend(app: FastAPI) -> None:
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/", response_class=HTMLResponse, include_in_schema=False)
    def home() -> str:
        return INDEX_FILE.read_text(encoding="utf-8")
