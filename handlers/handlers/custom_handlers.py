import asyncio

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import StateFilter
from sqlalchemy.ext.asyncio import AsyncSession

from config.config import CHANNEL_ID
from db.read_db import get_users_reader
from states.user_states import UserActionState
from keyboards.channel_keyborads import channel_post_keyboard
from db.write_db import add_manhva, get_or_create_manhva
from utils.manhva_names import manhva_names
from db.models import ManhvaUserAssociation

router = Router()


@router.message(StateFilter(UserActionState.add_manhva))
async def get_manhva_name(
    message: Message, state: FSMContext, session: AsyncSession, bot: Bot
):
    await add_manhva(
        session=session, user_id=message.from_user.id, names=message.text.split("//")
    )
    await state.set_state(state=None)
    await message.answer(
        "Манхва(ы) успешно добавлена.",
    )


# @router.message(StateFilter(UserActionState.remove_manhva))
# async def remove_manhva(
#     message: Message, state: FSMContext, session: AsyncSession, bot: Bot
# ):
#     await delete_manhva(
#         session=session, user_id=message.from_user.id, name=message.text
#     )
#     await state.set_state(state=None)
#     await message.answer("Манхва успешно удалена")


@router.message(F.from_user.id == 1920003379)
async def from_user_bot_handler(message: Message, session: AsyncSession, bot: Bot):
    manhva_content = message.text.split("\n")
    manhva_name = manhva_content[0]
    text = f"{manhva_name}\n{manhva_content[1]}\n\n{manhva_content[-1]}"
    manhva = await get_or_create_manhva(session=session, manhva_name=manhva_name)
    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=text,
        reply_markup=channel_post_keyboard(callback_data=int(manhva.id)),
    )
    await asyncio.sleep(2)
    if manhva_name in manhva_names.manhva_names():
        manhvas = await get_users_reader(session=session, manhva=manhva_name)
        for manhva in manhvas.user_details:  # type: ManhvaUserAssociation
            await bot.send_message(chat_id=manhva.user.user_id, text=text)
            await asyncio.sleep(1)
