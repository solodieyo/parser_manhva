from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from keyboards.inline_user_action import user_actions

router = Router()


@router.message(CommandStart())
async def bot_start(message: Message, bot: Bot) -> None:
    bot_information = await bot.get_me()
    await message.reply(f'Привет <b>{message.from_user.full_name}</b>', reply_markup=user_actions())
