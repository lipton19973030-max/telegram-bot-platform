from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from app.states.order_states import OrderStates
from app.keyboards.order_kb import service_keyboard, confirm_keyboard, remove_keyboard
from app.keyboards.user_kb import main_menu_keyboard
from app.services.order_service import OrderService
from app.services.notification_service import NotificationService

router = Router()

SERVICES = [
    "🔧 Сантехника",
    "⚡ Электрика",
    "🚪 Двери/замки",
    "👷 Разнорабочие",
    "📦 Грузчики",
    "🚚 Грузоперевозки",
    "🛋 Сборка мебели",
    "❄️ Сплит-системы",
    "🔨 Ремонт техники",
    "🗑 Вывоз мусора",
    "⛏ Демонтаж",
    "🌿 Покос травы",
    "🏠 Другое",
]


@router.message(F.text == "/neworder")
async def cmd_neworder(message: Message, state: FSMContext):
    await state.set_state(OrderStates.choosing_service)
    await message.answer(
        "Выберите тип услуги:",
        reply_markup=service_keyboard()
    )


@router.message(OrderStates.choosing_service, F.text == "❌ Отмена")
@router.message(OrderStates.entering_description, F.text == "❌ Отмена")
@router.message(OrderStates.confirming, F.text == "❌ Отменить")
async def cancel_order(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        f"Привет, {message.from_user.first_name}! 🙌\n\n"
        "Я ваш помощник в этом боте, помогу вам оставить заявку на услугу.",
        reply_markup=main_menu_keyboard()
    )


@router.message(OrderStates.choosing_service, F.text.in_(SERVICES))
async def service_chosen(message: Message, state: FSMContext):
    await state.update_data(service=message.text)
    await state.set_state(OrderStates.entering_description)
    await message.answer(
        f"Вы выбрали: {message.text}\n\nОпишите проблему подробнее:",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(OrderStates.entering_description)
async def description_entered(message: Message, state: FSMContext):
    data = await state.get_data()
    service = data.get("service")
    await state.update_data(description=message.text)
    await state.set_state(OrderStates.confirming)
    await message.answer(
        f"Проверьте заявку:\n\n"
        f"Услуга: {service}\n"
        f"Описание: {message.text}\n\n"
        f"Всё верно?",
        reply_markup=confirm_keyboard()
    )


@router.message(OrderStates.confirming, F.text == "✅ Подтвердить")
async def order_confirmed(message: Message, state: FSMContext, db_session, bot: Bot):
    data = await state.get_data()

    order_service = OrderService(db_session)
    order = await order_service.create_order(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        description=data.get("description"),
    )

    notification_service = NotificationService(bot)
    await notification_service.notify_admins_new_order(
        order_id=order.id,
        service=data.get("service"),
        description=data.get("description"),
        client_name=message.from_user.full_name,
        client_username=message.from_user.username,
        telegram_id=message.from_user.id,
    )

    await state.clear()
    await message.answer(
        f"✅ Заявка #{order.id} принята!\n"
        f"Услуга: {data.get('service')}\n"
        f"Описание: {data.get('description')}\n\n"
        f"Мы свяжемся с вами в ближайшее время.",
        reply_markup=main_menu_keyboard()
    )