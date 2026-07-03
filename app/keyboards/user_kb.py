from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 Создать заявку")],
            [KeyboardButton(text="📂 Мои заявки")],
            [KeyboardButton(text="❓ Помощь")],
        ],
        resize_keyboard=True,
    )
    return keyboard