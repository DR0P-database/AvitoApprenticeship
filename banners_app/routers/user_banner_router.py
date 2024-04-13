from . import *


user_banner_router = APIRouter(prefix='/user_banner', tags=["user_banner"])


@user_banner_router.get('/')
async def get_user_banner(
    banner_options: Annotated[SUserBannerGet, Depends()],
    x_token: str | None = Header(default=None)
) -> SUserBanner:

    is_admin = verify_token(token=x_token, is_user_allow=True)
    user_banner = await BannerRepository.get_user_banner(
        banner_options=banner_options,
        is_admin=is_admin)

    return user_banner
