import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

from config.settings import settings
from app.database.session import AsyncSessionLocal
from app.handlers import user
from aiogram import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from aiogram.types import TelegramObject


class DbSessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        async with AsyncSessionLocal() as session:
            data["session"] = session
            return await handler(event, data)


async def main():
    logger.info("Starting bot...")

    bot = Bot(token=settings.bot_token)
    dp = Dispatcher(storage=MemoryStorage())

    dp.update.middleware(DbSessionMiddleware())
    dp.include_router(user.router)

    logger.info(f"Bot {settings.bot_name} started!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())