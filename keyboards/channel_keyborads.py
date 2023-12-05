from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup


def channel_post_keyboard(callback_data: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Подписаться", callback_data=f"subscribe/{callback_data}")
    return builder.as_markup()
