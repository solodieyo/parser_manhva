from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from sqlalchemy.exc import IntegrityError, PendingRollbackError
from sqlalchemy.ext.asyncio import AsyncSession

from filter.manhva_name_callback import ManhvaSubscribeCallback

from db.write_db import add_manhva

router = Router()


@router.callback_query(ManhvaSubscribeCallback.filter(F.action == "subscribe"))
async def user_subscribe(
    callback: CallbackQuery,
    session: AsyncSession,
    callback_data: ManhvaSubscribeCallback,
):
    manhva_id = callback_data.manhva_id
    try:
        await add_manhva(_id=manhva_id, session=session, user_id=callback.from_user.id)
        await callback.answer(text="Вы успешно подписались")
    except (IntegrityError, PendingRollbackError):
        await callback.answer(text="Вы уже подписаны")
