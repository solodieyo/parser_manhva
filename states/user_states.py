from aiogram.fsm.state import StatesGroup, State


class UserActionState(StatesGroup):
	add_manhva = State()
	remove_manhva = State()
	archive_manhva = State()
	check_manhva_list = State()
	default_state = State()