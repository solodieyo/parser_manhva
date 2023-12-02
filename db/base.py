from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from config.config import user_name, password, host, port, db_name


def engine_string():
	result = f"postgresql+asyncpg://{user_name}:{password}@{host}:{port}/{db_name}"
	return result


Base = declarative_base()
meta_data = Base.metadata


session = async_sessionmaker(create_async_engine(engine_string()), expire_on_commit=False)


def create_session() -> AsyncSession:
	return session()
