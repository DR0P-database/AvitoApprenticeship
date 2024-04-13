from . import *

banner_router = APIRouter(prefix='/banner', tags=["user_banner"])


@banner_router.post('/')
async def add_banner(
    banner: SBannerAdd,
    token: Annotated[str | None, Header()] = None
) -> SBannerAdded:

    verify_token(token=token)
    banner_id = await BannerRepository.add_banner(banner)
    return JSONResponse(status_code=201, content={'banner_id': banner_id})


@banner_router.get('/', status_code=200)
async def get_banner(
    banner_options: Annotated[SBannerGet, Depends()],
    token: str | None = Header(default=None)
) -> list[SBanner]:

    verify_token(token=token)
    banners = await BannerRepository.get_banners(banner_options=banner_options)
    return banners
