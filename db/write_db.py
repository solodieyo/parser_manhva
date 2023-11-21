from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, update

from db.models import Manhva


async def add_manhva(names: List[str], user_id: int, session: AsyncSession):
	for name in names:
		record_manhva = Manhva()
		record_manhva.user_id = user_id
		record_manhva.manhva_name = name
		session.add(record_manhva)
	await session.commit()


async def delete_manhva(name: str, user_id: int, session: AsyncSession):
	await session.execute(delete(Manhva).where((Manhva.user_id == user_id) & (Manhva.manhva_name == name)))
	await session.commit()


async def archive_manhva(name: str, user_id: int, session: AsyncSession):
	await session.execute(update(Manhva).where((Manhva.user_id == user_id) & (Manhva.manhva_name == name))
						  .values(archived=True))
	await session.commit()