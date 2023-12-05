from aiogram import Bot, Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from keyboards.reply_action_keyboard import action_keyboard

router = Router()


@router.message(CommandStart())
async def bot_start(message: Message, bot: Bot) -> None:
    await message.reply(
        f"Привет <b>{message.from_user.full_name}</b>", reply_markup=action_keyboard()
    )
