from fastapi import HTTPException
from sqlalchemy import select

from .models import BannersOrm
from .database import new_session
from ..schemas.banner_schemas import *


class BannerRepository:
    @staticmethod
    async def add_one(data: SBannerAdd):
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
