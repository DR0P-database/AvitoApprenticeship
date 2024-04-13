from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import JSON, Column, Integer


class Model(DeclarativeBase):
    pass


class BannersOrm(Model):
    __tablename__ = 'banners'
    banner_id: Mapped[int] = mapped_column(primary_key=True)

    # Extra columns
    tag_ids: Mapped[list[int]] = mapped_column(ARRAY(Integer))
    feature_id: Mapped[int]
    content = Column(JSON)
    is_active: Mapped[bool]

    created_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc',now())"))
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc',now())"),
        onupdate=datetime.utcnow)
