import asyncio
from aiogram import Bot, Dispatcher
from loguru import logger

from config.settings import settings
from app.handlers import user


async def main():
    logger.info("Starting bot...")
    
    bot = Bot(token=settings.bot_token)
    dp = Dispatcher()
    
    # Подключаем роутеры
    dp.include_router(user.router)
    
    logger.info(f"Bot {settings.bot_name} started!")
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())