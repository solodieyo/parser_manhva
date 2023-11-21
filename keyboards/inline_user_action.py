from aiogram.utils.keyboard import InlineKeyboardBuilder


def user_actions():
	builder = InlineKeyboardBuilder()
	builder.button(text='New', callback_data='new')
	builder.button(text='Remove', callback_data='remove')
	builder.button(text='Archive', callback_data='arch')
	builder.button(text='List', callback_data='check')
	return builder.as_markup()
