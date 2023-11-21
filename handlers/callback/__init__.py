from aiogram import Router

from . import action_callback


def setup_callback_handlers():
	router = Router()
	router.include_router(action_callback.router)
	return router