from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from .models import Manhva


async def get_manhva_names(session: AsyncSession, user_id):
	names = await session.execute(select(Manhva.manhva_name)
								  .where((Manhva.user_id == user_id) & (Manhva.archived == False)))
	names = names.scalars().all()
	return names


async def get_users_reader(session: AsyncSession, manhva: str):
	users = await session.execute(select(Manhva.user_id)
								  .where((Manhva.manhva_name == manhva) & (Manhva.archived == False)))
	return users.scalars().all()