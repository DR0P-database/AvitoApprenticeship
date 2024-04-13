from datetime import datetime
from pydantic import BaseModel


class SUserBannerGet(BaseModel):
    feature_id: int
    tag_id: int
    use_last_revision: bool | None = False


class SUserBanner(BaseModel):
    content: dict


class SBannerGet(BaseModel):
    feature_id: int | None = None
    tag_id: int | None = None
    limit: int | None = None
    offset: int | None = None


class SBannerAdd(BaseModel):
    tag_ids: list[int] = []
    feature_id: int
    content: dict
    is_active: bool


# Pydantic schema to response router when added Banner
class SBannerAdded(BaseModel):
    banner_id: int


class SBanner(SBannerAdd):
    banner_id: int
    created_at: datetime
    updated_at: datetime


class SBannerPatch(BaseModel):
    tag_ids: list[int] | None = None
    feature_id: int | None = None
    content: dict | None = None
    is_active: bool | None = None
