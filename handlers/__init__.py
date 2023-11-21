from aiogram import Router

from . import start
from . import custom_handlers
from .callback import setup_callback_handlers


def get_handlers_router():
	setup_router = Router()
	setup_router.include_router(start.router)
	setup_router.include_router(setup_callback_handlers())
	setup_router.include_router(custom_handlers.router)
	return setup_router