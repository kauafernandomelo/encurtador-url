from datetime import datetime

from pydantic import AnyHttpUrl, BaseModel, ConfigDict


class CreateShortUrlRequest(BaseModel):
    url: AnyHttpUrl


class ShortUrlResponse(BaseModel):
    code: str
    original_url: str
    short_url: str
    access_count: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
