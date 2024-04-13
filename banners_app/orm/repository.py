from fastapi import HTTPException
from sqlalchemy import select

from .models import BannersOrm
from .database import new_session
from ..schemas.banner_schemas import *


class BannerRepository:
    @staticmethod
    async def add_banner(data: SBannerAdd):
        async with new_session() as session:

            query = (
                select(BannersOrm)
                .where(BannersOrm.feature_id == data.feature_id)
                .where(BannersOrm.tag_ids == data.tag_ids)
            )
            result = await session.execute(query)
            if result.scalars().all():
                raise HTTPException(
                    status_code=400, detail='Такой баннер уже есть')

            banner_dict = data.model_dump()
            banner = BannersOrm(**banner_dict)
            session.add(banner)
            await session.flush()
            banner_id = banner.banner_id
            await session.commit()
            return banner_id

    @staticmethod
    async def get_banners(banner_options) -> list[SBanner]:
        async with new_session() as session:
            query = select(BannersOrm)

            if banner_options.feature_id is not None:
                query = query.filter(
                    BannersOrm.feature_id == banner_options.feature_id)
            if banner_options.tag_id is not None:
                query = query.where(
                    BannersOrm.tag_ids.any(banner_options.tag_id))
            if banner_options.offset is not None:
                query = query.offset(banner_options.offset)
            if banner_options.limit is not None:
                query = query.limit(banner_options.limit)

            result = await session.execute(query)
            banner_models = result.scalars().all()

            banner_schemas = [SBanner.model_validate(
                banner_orm, from_attributes=True) for banner_orm in banner_models]

            return banner_schemas
