from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator
from app.core.config import settings
from sqlmodel import SQLModel

# create engine
engine = create_async_engine(
    url = settings.DATABASE_URL, 
    echo = True
)

#create session
async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


# populating db 
async def create_db():
    async with engine.begin() as conn : 
        await conn.run_sync(SQLModel.metadata.create_all)

#provide session
async def get_session() -> AsyncGenerator[AsyncSession, None]: 
    async with async_session() as session : 
        yield  session 
