from typing import List

from sqlalchemy.exc import NoResultFound, IntegrityError, PendingRollbackError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, update, select, and_
from sqlalchemy.orm import selectinload

from db.models import Manhva, User, ManhvaUserAssociation
from utils.manhva_names import manhva_names


async def add_manhva(
    user_id: int, session: AsyncSession, names: List[str] = None, _id: int = None
):
    user = await get_or_create_user(session=session, user_id=user_id)
    if _id:
        manhva = await get_manhva_for_id(session=session, _id=_id)
        user.manhva_details.append(ManhvaUserAssociation(manhva=manhva))
        await session.commit()
    else:
        for name in names:
            manhva = await get_or_create_manhva(session=session, manhva_name=name)
            user.manhva_details.append(ManhvaUserAssociation(manhva=manhva))
            try:
                await session.commit()
            except (IntegrityError, PendingRollbackError):
                continue
    await manhva_names.refresh_list()


async def delete_manhva(name: str, user_id: int, session: AsyncSession):
    user = await get_or_create_user(session=session, user_id=user_id)
    manhva = await get_or_create_manhva(session=session, manhva_name=name)
    await session.execute(
        delete(ManhvaUserAssociation).where(
            and_(
                ManhvaUserAssociation.manhva_id == manhva.id,
                ManhvaUserAssociation.user_id == user.id,
            )
        )
    )
    await session.commit()
    await manhva_names.refresh_list()


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


async def get_or_create_manhva(session: AsyncSession, manhva_name: str):
    stmt = select(Manhva).where(Manhva.manhva_name == manhva_name)
    instance = await session.scalars(stmt)
    try:
        return instance.one()
    except NoResultFound:
        instance = Manhva(manhva_name=manhva_name)
        session.add(instance)
        await session.commit()
        return instance


async def get_manhva_for_id(session: AsyncSession, _id: int):
    stmt = select(Manhva).where(Manhva.id == _id)
    instance = await session.scalars(stmt)
    return instance.one()
