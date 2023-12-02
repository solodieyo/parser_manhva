import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums.parse_mode import ParseMode

from middleware.db_session import DBSessionMiddleware
from config import config
from handlers import get_handlers_router
from utils.manhva_names import manhva_names


async def main():
    await manhva_names.refresh_list()
    bot = Bot(token=config.bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(get_handlers_router())
    dp.update.middleware(DBSessionMiddleware(session_pool=session))
    await bot.delete_webhook(drop_pending_updates=True)
    print(manhva_names.get_names())
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        print(123)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('end work1')
