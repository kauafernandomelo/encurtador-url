from datetime import UTC, datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from url_shortener.database import Base


class ShortUrl(Base):
    __tablename__ = "short_urls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    original_url: Mapped[str] = mapped_column(String(2048), nullable=False)
    code: Mapped[str] = mapped_column(
        String(32), unique=True, index=True, nullable=False
    )
    access_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
