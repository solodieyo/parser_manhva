from aiogram import Router

from . import user_action, custom_handlers


def setup_custom_handlers():
    router = Router()
    router.include_router(user_action.router)
    router.include_router(custom_handlers.router)
    return router
