from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from url_shortener.config import Settings, get_settings
from url_shortener.database import get_db_session
from url_shortener.repository import ShortUrlRepository
from url_shortener.schemas import CreateShortUrlRequest, ShortUrlResponse
from url_shortener.service import ShortUrlNotFoundError, ShortUrlService

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_db_session)]
SettingsDep = Annotated[Settings, Depends(get_settings)]


def get_short_url_service(
    session: SessionDep,
    settings: SettingsDep,
) -> ShortUrlService:
    repository = ShortUrlRepository(session)
    return ShortUrlService(repository=repository, code_size=settings.short_code_size)


ServiceDep = Annotated[ShortUrlService, Depends(get_short_url_service)]


def build_short_url(request: Request, code: str, settings: Settings) -> str:
    base_url = settings.base_url.rstrip("/") or str(request.base_url).rstrip("/")
    return f"{base_url}/{code}"


@router.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@router.post(
    "/api/urls",
    response_model=ShortUrlResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["urls"],
)
def create_short_url(
    payload: CreateShortUrlRequest,
    request: Request,
    service: ServiceDep,
    settings: SettingsDep,
) -> ShortUrlResponse:
    short_url = service.create_short_url(str(payload.url))
    return ShortUrlResponse(
        code=short_url.code,
        original_url=short_url.original_url,
        short_url=build_short_url(request, short_url.code, settings),
        access_count=short_url.access_count,
        created_at=short_url.created_at,
    )


@router.get("/api/urls/{code}", response_model=ShortUrlResponse, tags=["urls"])
def get_short_url_stats(
    code: str,
    request: Request,
    service: ServiceDep,
    settings: SettingsDep,
) -> ShortUrlResponse:
    try:
        short_url = service.get_stats(code)
    except ShortUrlNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL encurtada não encontrada.",
        ) from exc

    return ShortUrlResponse(
        code=short_url.code,
        original_url=short_url.original_url,
        short_url=build_short_url(request, short_url.code, settings),
        access_count=short_url.access_count,
        created_at=short_url.created_at,
    )


@router.get("/{code}", tags=["redirects"])
def redirect_to_original_url(
    code: str,
    service: ServiceDep,
) -> RedirectResponse:
    try:
        original_url = service.get_original_url(code)
    except ShortUrlNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL encurtada não encontrada.",
        ) from exc

    return RedirectResponse(
        url=original_url,
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )
