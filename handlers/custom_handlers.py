import asyncio

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import StateFilter
from sqlalchemy.ext.asyncio import AsyncSession

from db.read_db import get_users_reader
from states.user_states import UserActionState
from keyboards.inline_user_action import user_actions
from db.write_db import add_manhva, delete_manhva, archive_manhva
from utils.manhva_names import manhva_names

router = Router()


@router.message(StateFilter(UserActionState.add_manhva))
async def get_manhva_name(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    await add_manhva(session=session, user_id=message.from_user.id, names=message.text.split('//'))
    await state.set_state(state=None)
    await message.answer('Манхва(ы) успешно добавлена. List чтобы посмотреть все манхвы.', reply_markup=user_actions())


@router.message(StateFilter(UserActionState.remove_manhva))
async def remove_manhva(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    await delete_manhva(session=session, user_id=message.from_user.id, name=message.text)
    await state.set_state(state=None)
    await message.answer('Манхва успешно удалена', reply_markup=user_actions())


@router.message(StateFilter(UserActionState.archive_manhva))
async def arch_manhva(message: Message, state: FSMContext, session: AsyncSession, bot: Bot):
    await archive_manhva(session=session, user_id=message.from_user.id, name=message.text)
    await state.set_state(state=None)
    await message.answer('Манхва успешно архивирована', reply_markup=user_actions())


@router.message(F.from_user.id == 1920003379)
async def from_user_bot_handler(message: Message, session: AsyncSession, bot: Bot):
    manhva_content = message.text.split('\n')
    manhva_name = manhva_content[0]
    text = f'{manhva_name}\n{manhva_content[1]}\n\n{manhva_content[-1]}'
    if manhva_name in manhva_names.get_names():
        users = await get_users_reader(session=session, manhva=manhva_name)
        for user in users:
            await bot.send_message(chat_id=user, text=text)
            await asyncio.sleep(0.5)
