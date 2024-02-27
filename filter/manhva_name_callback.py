from aiogram.filters.callback_data import CallbackData


class ManhvaSubscribeCallback(CallbackData, prefix="user"):
    action: str
    manhva_id: int
