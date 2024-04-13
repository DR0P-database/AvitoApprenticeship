from . import *

banner_router = APIRouter(prefix='/banner', tags=["user_banner"])


@banner_router.post('/')
async def add_banner(banner: SBannerAdd, token: Annotated[str | None, Header()] = None) -> SBannerAdded:
    verify_token(token=token)
    banner_id = await BannerRepository.add_one(banner)
    return JSONResponse(status_code=201, content={'banner_id': banner_id})
