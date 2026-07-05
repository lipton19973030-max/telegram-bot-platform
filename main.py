import asyncio
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config.settings import settings
from app.middlewares.db import DbSessionMiddleware
from app.database.session import AsyncSessionLocal
from app.handlers import user
from app.handlers import order_fsm
from app.handlers import my_orders
from app.handlers import admin


async def main():
    logger.info(f"Starting bot {settings.bot_name}...")
    bot = Bot(token=settings.bot_token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)

    dp.update.middleware(DbSessionMiddleware(AsyncSessionLocal))

    dp.include_router(user.router)
    dp.include_router(order_fsm.router)
    dp.include_router(my_orders.router)
    dp.include_router(admin.router)

    logger.info(f"Bot {settings.bot_name} started!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())