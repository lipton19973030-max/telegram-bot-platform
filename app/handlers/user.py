from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from app.states.order_states import OrderStates
from app.keyboards.order_kb import service_keyboard
from app.keyboards.user_kb import main_menu_keyboard

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! 🙌\n\n"
        "Я ваш помощник в этом боте, помогу вам оставить заявку на услугу.",
        reply_markup=main_menu_keyboard()
    )


@router.message(Command("help"))
@router.message(F.text == "❓ Помощь")
async def cmd_help(message: Message):
    await message.answer(
        "Доступные команды:\n\n"
        "📋 Создать заявку — /neworder\n"
        "📂 Мои заявки — /myorders\n"
        "❓ Помощь — /help"
    )


@router.message(Command("myorders"))
@router.message(F.text == "📂 Мои заявки")
async def cmd_myorders(message: Message):
    await message.answer("Функция в разработке. Скоро будет доступна!")


@router.message(F.text == "📋 Создать заявку")
async def btn_neworder(message: Message, state: FSMContext):
    await state.set_state(OrderStates.choosing_service)
    await message.answer(
        "Выберите тип услуги:",
        reply_markup=service_keyboard()
    )