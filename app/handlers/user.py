from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.client import ClientRepository

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession):
    repo = ClientRepository(session)
    client = await repo.get_or_create(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )

    text = (
        f"Привет, {message.from_user.first_name}! 👋\n"
        f"Я бот для сервисных компаний.\n"
        f"Используй /help для списка команд."
    )
    await message.answer(text)