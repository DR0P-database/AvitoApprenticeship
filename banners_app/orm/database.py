from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from ..config import settings
from .models import Model


engine = create_async_engine(
    url=settings.database_url_asyncpg,
    echo=True
)

new_session = async_sessionmaker(engine, expire_on_commit=True)


async def create_tables():
    async with engine.begin() as conn:
        # metadata хранит все таблицы которые мы создали в python
        # metadata_obj.create_all(engine) создает все таблицы которые есть в metadata
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
