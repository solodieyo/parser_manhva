from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from db.read_db import get_user_manhva
from db.models import ManhvaUserAssociation
from states.user_states import UserActionState

router = Router()


@router.message(F.text == "Добавить")
async def new_manhva_callback(message: Message, state: FSMContext):
    await message.answer(
        "Введите манхвы которые хотите добавить(через // например манхва1//манхва2//манхва3)."
    )
    await state.set_state(state=UserActionState.add_manhva)


@router.message(F.text == "Удалить")
async def new_manhva_callback(message: Message, state: FSMContext):
    await message.answer("Введите название манхвы которую хотите удалить.")
    await state.set_state(state=UserActionState.remove_manhva)


@router.message(F.text == "Список")
async def new_manhva_callback(message: Message, session: AsyncSession):
    user = await get_user_manhva(session=session, user_id=message.from_user.id)
    text = ""

    if user:
        for index, user_details in enumerate(
            user.manhva_details
        ):  # type: ManhvaUserAssociation
            text += f"{index+1}) {user_details.manhva.manhva_name}\n"
        await message.answer(
            text=f"{message.from_user.mention_html()}\n<b>Ваш список отслеживания:</b>\n{text}"
        )
    else:
        await message.answer(text=f"Ваш список отслеживания:\nПуст")
