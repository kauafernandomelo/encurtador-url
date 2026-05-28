from sqlalchemy import select
from sqlalchemy.orm import Session

from url_shortener.models import ShortUrl


class ShortUrlRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_code(self, code: str) -> ShortUrl | None:
        statement = select(ShortUrl).where(ShortUrl.code == code)
        return self._session.scalar(statement)

    def create(self, original_url: str, code: str) -> ShortUrl:
        short_url = ShortUrl(original_url=original_url, code=code)
        self._session.add(short_url)
        self._session.commit()
        self._session.refresh(short_url)
        return short_url

    def increment_access_count(self, short_url: ShortUrl) -> ShortUrl:
        short_url.access_count += 1
        self._session.commit()
        self._session.refresh(short_url)
        return short_url
