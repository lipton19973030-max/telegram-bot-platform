from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


def service_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔧 Сантехника"), KeyboardButton(text="⚡ Электрика")],
            [KeyboardButton(text="🚪 Двери/замки"), KeyboardButton(text="👷 Разнорабочие")],
            [KeyboardButton(text="📦 Грузчики"), KeyboardButton(text="🚚 Грузоперевозки")],
            [KeyboardButton(text="🛋 Сборка мебели"), KeyboardButton(text="❄️ Сплит-системы")],
            [KeyboardButton(text="🔨 Ремонт техники"), KeyboardButton(text="🗑 Вывоз мусора")],
            [KeyboardButton(text="⛏ Демонтаж"), KeyboardButton(text="🌿 Покос травы")],
            [KeyboardButton(text="🏠 Другое")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def confirm_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Подтвердить"), KeyboardButton(text="❌ Отменить")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()