from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.client import ClientRepository
from app.services.order_service import OrderService

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


@router.message(Command("neworder"))
async def cmd_new_order(message: Message, session: AsyncSession):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer(
            "Укажи описание заявки.\n"
            "Пример: /neworder Сломался кран на кухне"
        )
        return

    description = args[1]
    service = OrderService(session)
    order = await service.create_order(
        telegram_id=message.from_user.id,
        description=description,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
    )

    await message.answer(
        f"✅ Заявка #{order.id} создана!\n"
        f"Описание: {order.description}\n"
        f"Статус: {order.status.value}"
    )


@router.message(Command("myorders"))
async def cmd_my_orders(message: Message, session: AsyncSession):
    service = OrderService(session)
    orders = await service.get_client_orders(message.from_user.id)

    if not orders:
        await message.answer("У тебя пока нет заявок. Создай первую: /neworder")
        return

    text = "📋 Твои заявки:\n\n"
    for order in orders:
        text += f"#{order.id} — {order.status.value}\n{order.description}\n\n"

    await message.answer(text)


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Доступные команды:\n\n"
        "/start — начать работу\n"
        "/neworder [описание] — создать заявку\n"
        "/myorders — мои заявки\n"
        "/help — помощь"
    )