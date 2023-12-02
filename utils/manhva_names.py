from sqlalchemy.ext.asyncio import AsyncSession

from db.read_db import get_all_manhva_names
from db.base import create_session


class ManhvaName:
    __manhva_names = []

    async def refresh_list(self):
        async with create_session() as session:
            self.__manhva_names = await get_all_manhva_names(session=session)

    def get_names(self):
        return self.__manhva_names


manhva_names = ManhvaName()
