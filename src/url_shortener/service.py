import secrets
import string

from url_shortener.models import ShortUrl
from url_shortener.repository import ShortUrlRepository


class ShortUrlNotFoundError(Exception):
    pass


class ShortUrlService:
    _alphabet = string.ascii_letters + string.digits

    def __init__(self, repository: ShortUrlRepository, code_size: int) -> None:
        self._repository = repository
        self._code_size = code_size

    def create_short_url(self, original_url: str) -> ShortUrl:
        code = self._generate_unique_code()
        return self._repository.create(original_url=original_url, code=code)

    def get_original_url(self, code: str) -> str:
        short_url = self._repository.get_by_code(code)
        if short_url is None:
            raise ShortUrlNotFoundError

        self._repository.increment_access_count(short_url)
        return short_url.original_url

    def get_stats(self, code: str) -> ShortUrl:
        short_url = self._repository.get_by_code(code)
        if short_url is None:
            raise ShortUrlNotFoundError
        return short_url

    def _generate_unique_code(self) -> str:
        while True:
            code = "".join(
                secrets.choice(self._alphabet) for _ in range(self._code_size)
            )
            if self._repository.get_by_code(code) is None:
                return code
