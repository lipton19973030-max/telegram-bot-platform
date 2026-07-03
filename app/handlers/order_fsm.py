from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from app.states.order_states import OrderStates
from app.keyboards.order_kb import service_keyboard, confirm_keyboard, remove_keyboard
from app.services.order_service import OrderService

router = Router()

SERVICES = [
    "🔧 Сантехника", "⚡ Электрика", "🚪 Двери/замки", "👷 Разнорабочие",
    "📦 Грузчики", "🚚 Грузоперевозки", "🛋 Сборка мебели", "❄️ Сплит-системы",
    "🔨 Ремонт техники", "🗑 Вывоз мусора", "⛏ Демонтаж", "🌿 Покос травы",
    "🏠 Другое",
]


@router.message(F.text == "/neworder")
async def cmd_neworder(message: Message, state: FSMContext):
    await state.set_state(OrderStates.choosing_service)
    await message.answer(
        "Выберите тип услуги:",
        reply_markup=service_keyboard()
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
async def order_confirmed(message: Message, state: FSMContext, db_session):
    data = await state.get_data()
    order_service = OrderService(db_session)
    order = await order_service.create_order(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        description=data.get("description"),
    )
    await state.clear()
    await message.answer(
        f"✅ Заявка #{order.id} принята!\n"
        f"Услуга: {data.get('service')}\n"
        f"Описание: {data.get('description')}\n\n"
        f"Мы свяжемся с вами в ближайшее время.",
        reply_markup=remove_keyboard()
    )


@router.message(OrderStates.confirming, F.text == "❌ Отменить")
async def order_cancelled(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Заявка отменена. Напишите /neworder чтобы начать заново.",
        reply_markup=remove_keyboard()
    )