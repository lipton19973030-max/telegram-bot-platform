from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n\n"
        "Я помогу вам оставить заявку на услугу.\n\n"
        "Доступные команды:\n"
        "/neworder — создать заявку\n"
        "/myorders — мои заявки\n"
        "/help — помощь"
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Доступные команды:\n\n"
        "/start — начать работу\n"
        "/neworder — создать заявку\n"
        "/myorders — мои заявки\n"
        "/help — помощь"
    )


@router.message(Command("myorders"))
async def cmd_myorders(message: Message):
    await message.answer("Функция в разработке. Скоро будет доступна!")