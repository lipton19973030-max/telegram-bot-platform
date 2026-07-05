from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from app.states.order_states import OrderStates
from app.keyboards.order_kb import service_keyboard
from app.keyboards.user_kb import main_menu_keyboard

router = Router()


def support_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💬 Написать в поддержку",
                    url="https://t.me/adm_uslugi_andrey"
                )
            ]
        ]
    )


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
        "Если у вас возникли вопросы или проблемы — напишите нам, мы поможем! 👇",
        reply_markup=support_keyboard()
    )


@router.message(F.text == "📋 Создать заявку")
async def btn_neworder(message: Message, state: FSMContext):
    await state.set_state(OrderStates.choosing_service)
    await message.answer(
        "Выберите тип услуги:",
        reply_markup=service_keyboard()
    )