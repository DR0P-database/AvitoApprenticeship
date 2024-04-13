from sqlalchemy.dialects.postgresql import array
from fastapi import HTTPException
from sqlalchemy import or_, select

from .models import BannersOrm
from .database import new_session
from ..schemas.banner_schemas import *


class BannerRepository:
    @staticmethod
    async def get_user_banner(banner_options: SUserBannerGet, is_admin) -> SUserBanner:
        async with new_session() as session:
            query = (
                select(BannersOrm)
                .filter(BannersOrm.feature_id == banner_options.feature_id)
                .where(BannersOrm.tag_ids.any(banner_options.tag_id))
                .filter(or_(BannersOrm.is_active == (not is_admin), BannersOrm.is_active))
            )

            if banner_options.use_last_revision:  # Some add
                query = query

            result = await session.execute(query)
            result = result.scalars().first()
            if not result:
                raise HTTPException(
                    status_code=404, detail='Баннер для не найден')

            banner = SUserBanner.model_validate(
                result, from_attributes=True)

            return banner

    @staticmethod
    async def add_banner(data: SBannerAdd):
        async with new_session() as session:

            query = (
                select(BannersOrm)
                .where(BannersOrm.feature_id == data.feature_id)
                .where(BannersOrm.tag_ids.overlap(data.tag_ids))
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

    @staticmethod
    async def patch_banner(id: int, patch_banner: SBannerPatch):
        async with new_session() as session:
            banner = await session.get(BannersOrm, id)

            # Verify 1 If banner by id exists
            if banner:
                if patch_banner.tag_ids is not None:
                    banner.tag_ids = array(
                        patch_banner.tag_ids, type_=int)
                if patch_banner.feature_id is not None:
                    banner.feature_id = patch_banner.feature_id
                if patch_banner.content is not None:
                    banner.content = patch_banner.content
                if patch_banner.is_active is not None:
                    banner.is_active = patch_banner.is_active
            else:
                raise HTTPException(status_code=404, detail='Баннер не найден')

            # Verify 2 If banner with same options exists
            query = (
                select(BannersOrm)
                .where(BannersOrm.banner_id != banner.banner_id)
                .where(BannersOrm.feature_id == banner.feature_id)
                .where(BannersOrm.tag_ids.overlap(banner.tag_ids))
            )
            result = await session.execute(query)
            if result.scalars().all():
                raise HTTPException(
                    status_code=400, detail='Похожий баннер уже есть')

            await session.flush()
            await session.commit()
