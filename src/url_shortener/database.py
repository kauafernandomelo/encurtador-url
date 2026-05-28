from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from url_shortener.config import get_settings


class Base(DeclarativeBase):
    pass


def create_database_engine(database_url: str) -> Engine:
    connect_args = (
        {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    )
    return create_engine(database_url, connect_args=connect_args)


engine = create_database_engine(get_settings().database_url)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


def get_db_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
