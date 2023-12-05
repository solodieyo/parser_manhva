from aiogram import Router

from . import subscribe_callback


def setup_callback_handlers():
    router = Router()
    router.include_router(subscribe_callback.router)
    return router
