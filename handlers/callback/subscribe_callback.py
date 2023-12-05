from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from sqlalchemy.ext.asyncio import AsyncSession

from db.write_db import add_manhva

router = Router()


@router.callback_query(F.data.startswith("subscribe"))
async def user_subscribe(callback: CallbackQuery, session: AsyncSession):
    manhva_name = callback.data.split("/")[0:]
    try:
        await add_manhva(
            names=manhva_name, session=session, user_id=callback.from_user.id
        )
        await callback.answer(text="Вы успешно подписались")
    except (IntegrityError, PendingRollbackError):
        await callback.answer(text="Вы уже подписаны")
