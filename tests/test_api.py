from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from url_shortener.config import Settings, get_settings
from url_shortener.database import Base, get_db_session
from url_shortener.main import create_app


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db_session() -> Generator[Session, None, None]:
        session = TestingSessionLocal()
        try:
            yield session
        finally:
            session.close()

    def override_get_settings() -> Settings:
        return Settings(base_url="http://testserver", database_url="sqlite:///:memory:")

    app = create_app(create_database=False)
    app.dependency_overrides[get_db_session] = override_get_db_session
    app.dependency_overrides[get_settings] = override_get_settings

    with TestClient(app) as test_client:
        yield test_client


def test_create_short_url(client: TestClient) -> None:
    response = client.post("/api/urls", json={"url": "https://example.com/artigo"})

    assert response.status_code == 201
    body = response.json()
    assert body["original_url"] == "https://example.com/artigo"
    assert body["short_url"] == f"http://testserver/{body['code']}"
    assert body["access_count"] == 0


def test_home_page_loads(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert "Encurtador de URL" in response.text
    assert "Tecnologias utilizadas" in response.text
    assert "/static/app.js" in response.text


def test_static_css_loads(client: TestClient) -> None:
    response = client.get("/static/styles.css")

    assert response.status_code == 200
    assert "hero-card" in response.text


def test_redirect_to_original_url(client: TestClient) -> None:
    created = client.post("/api/urls", json={"url": "https://example.com"}).json()

    response = client.get(f"/{created['code']}", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com/"


def test_redirect_increments_access_count(client: TestClient) -> None:
    created = client.post("/api/urls", json={"url": "https://example.com"}).json()

    client.get(f"/{created['code']}", follow_redirects=False)
    stats = client.get(f"/api/urls/{created['code']}")

    assert stats.status_code == 200
    assert stats.json()["access_count"] == 1


def test_invalid_url_returns_validation_error(client: TestClient) -> None:
    response = client.post("/api/urls", json={"url": "not-a-url"})

    assert response.status_code == 422


def test_unknown_code_returns_not_found(client: TestClient) -> None:
    response = client.get("/codigo-inexistente", follow_redirects=False)

    assert response.status_code == 404
