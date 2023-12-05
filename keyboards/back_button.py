from aiogram.utils.keyboard import InlineKeyboardBuilder


def back_button():
    builder = InlineKeyboardBuilder()
    builder.button(text="Back", callback_data="back")
    return builder.as_markup()
