from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from .models import Manhva, User, ManhvaUserAssociation


async def get_all_manhva_names(session: AsyncSession):
    names = await session.execute(select(Manhva.manhva_name))
    names = names.scalars().all()
    return names


async def get_user_manhva(session: AsyncSession, user_id: int):
    try:
        stmt = (
            select(User)
            .where(User.user_id == user_id)
            .options(
                selectinload(User.manhva_details).joinedload(
                    ManhvaUserAssociation.manhva
                )
            )
        )
        user = await session.scalar(stmt)
        return user
    except NoResultFound:
        return None


async def get_users_reader(session: AsyncSession, manhva: str):
    stmt = (
        select(Manhva)
        .where(Manhva.manhva_name == manhva)
        .options(
            selectinload(Manhva.user_details).joinedload(ManhvaUserAssociation.user)
        )
    )
    users = await session.scalars(stmt)
    return users.one()
