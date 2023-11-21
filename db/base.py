from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.config import user_name, password, host, port, db_name


def engine_string():
	result = f"postgresql+asyncpg://{user_name}:{password}@{host}:{port}/{db_name}"
	return result


Base = declarative_base()
meta_data = Base.metadata

engine = create_async_engine(url=engine_string())

session = async_sessionmaker(engine, expire_on_commit=False)
