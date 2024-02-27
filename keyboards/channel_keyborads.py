from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from db.write_db import get_or_create_manhva
from filter.manhva_name_callback import ManhvaSubscribeCallback


def channel_post_keyboard(callback_data: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Подписаться",
        callback_data=ManhvaSubscribeCallback(
            action="subscribe", manhva_id=callback_data
        ),
    )
    return builder.as_markup()
