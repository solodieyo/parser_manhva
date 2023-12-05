from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton


def action_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="Добавить"), KeyboardButton(text="Удалить"))
    builder.row(KeyboardButton(text="Список"))
    builder.adjust(3, repeat=True)
    return builder.as_markup()
