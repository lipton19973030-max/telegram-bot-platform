import asyncio
import logging
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config.settings import settings


async def main():
    logging.basicConfig(level=logging.INFO)
    logger.info("Starting bot...")

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()

    logger.info(f"Bot {settings.bot_name} started!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
