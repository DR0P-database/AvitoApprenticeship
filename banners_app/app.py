from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


from .orm.database import create_tables, delete_tables
from .routers.user_banner_router import user_banner_router
from .routers.banner_router import banner_router
from .redis_tools.redis_settings import MyRedis

rd = None


async def lifespan(app: FastAPI):
    try:
        MyRedis.connect_redis()
    except:
        pass
    try:
        # await delete_tables()
        await create_tables()
    except:
        pass
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(user_banner_router)
app.include_router(banner_router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={'error': 'Некорректные данные'}
    )


@app.exception_handler(500)
async def internal_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Внутренняя ошибка сервера"}
    )
