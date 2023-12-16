from typing import List

from sqlalchemy.exc import NoResultFound, IntegrityError, PendingRollbackError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, update, select
from sqlalchemy.orm import selectinload

from db.models import Manhva, User, ManhvaUserAssociation
from utils.manhva_names import manhva_names


async def add_manhva(user_id: int, session: AsyncSession, names: List[str] = None, _id: int = None):
    user = await get_or_create_user(session=session, user_id=user_id)
    if _id:
        await write_manhva_db(session=session, _id=_id, user=user)
    for name in names:
        await write_manhva_db(user=user, session=session, _id=_id, manhva_name=name)
        try:
            await session.commit()
        except (IntegrityError, PendingRollbackError):
            continue
    await manhva_names.refresh_list()


async def write_manhva_db(user, session: AsyncSession, _id: int = None, manhva_name: str = None):
    manhva = await get_or_create_manhva(session=session, manhva_name=manhva_name)
    user.manhva_details.append(ManhvaUserAssociation(manhva=manhva))


async def delete_manhva(name: str, user_id: int, session: AsyncSession):
    await session.execute(
        delete(Manhva).where((Manhva.user_id == user_id) & (Manhva.manhva_name == name))
    )
    await manhva_names.refresh_list()
    await session.commit()


async def get_or_create_user(session: AsyncSession, user_id: int):
    stmt = (
        select(User)
        .where(User.user_id == user_id)
        .options(selectinload(User.manhva_details))
    )
    instance = await session.scalars(stmt)

    try:
        return instance.one()
    except NoResultFound:
        new_user = User(user_id=user_id)
        session.add(new_user)
        await session.commit()
        return new_user


async def get_or_create_manhva(session: AsyncSession, manhva_name: str = None, _id: int = None):
    if manhva_name:
        stmt = select(Manhva).where(Manhva.manhva_name == manhva_name)
    else:
        stmt = select(Manhva).where(Manhva.id == _id)
    instance = await session.scalars(stmt)
    try:
        return instance.one()
    except NoResultFound:
        instance = Manhva(manhva_name=manhva_name)
        session.add(instance)
        await session.commit()
        print("manhva", instance)
        return instance
