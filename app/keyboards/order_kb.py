from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

SERVICES = [
    "🔧 Сантехника", "⚡ Электрика", "🚪 Двери/замки", "👷 Разнорабочие",
    "📦 Грузчики", "🚚 Грузоперевозки", "🛋 Сборка мебели", "❄️ Сплит-системы",
    "🔨 Ремонт техники", "🗑 Вывоз мусора", "⛏ Демонтаж", "🌿 Покос травы",
    "🏠 Другое",
]


def service_keyboard() -> ReplyKeyboardMarkup:
    buttons = [[KeyboardButton(text=s)] for s in SERVICES]
    buttons.append([KeyboardButton(text="❌ Отмена")])
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def description_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Отмена")]],
        resize_keyboard=True
    )


def confirm_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ Подтвердить")],
            [KeyboardButton(text="❌ Отмена")],
        ],
        resize_keyboard=True
    )


def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()