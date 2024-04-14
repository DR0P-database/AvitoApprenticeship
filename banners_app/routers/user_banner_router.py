from . import *


user_banner_router = APIRouter(prefix='/user_banner', tags=["user_banner"])


@user_banner_router.get('/')
async def get_user_banner(
    banner_options: Annotated[SUserBannerGet, Depends()],
    x_token: str | None = Header(default=None),
    session: AsyncSession = Depends(get_async_session)
) -> SUserBanner:
    is_admin = verify_token(token=x_token, is_user_allow=True)

    full_request_str = banner_options.model_dump_json() + x_token

    cached_banner = MyRedis.rd.get(full_request_str)
    if not cached_banner or banner_options.use_last_revision:
        user_banner = await BannerRepository.get_user_banner(
            session,
            banner_options=banner_options,
            is_admin=is_admin)
        MyRedis.rd.setex(full_request_str, 5*60, user_banner.model_dump_json())
        return user_banner
    else:
        return SUserBanner.model_validate_json(cached_banner)
