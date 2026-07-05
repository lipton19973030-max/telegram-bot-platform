from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

from app.keyboards.user_kb import main_menu_keyboard
from app.services.order_service import OrderService
from app.models.order import OrderStatus

router = Router()

STATUS_EMOJI = {
    OrderStatus.new: "🆕 Новая",
    OrderStatus.in_progress: "⚙️ В работе",
    OrderStatus.done: "✅ Выполнена",
    OrderStatus.cancelled: "❌ Отменена",
}

ACTIVE_STATUSES = (OrderStatus.new, OrderStatus.in_progress)


def orders_list_keyboard(orders: list) -> InlineKeyboardMarkup:
    buttons = []
    for order in orders:
        status_text = STATUS_EMOJI.get(order.status, order.status)
        buttons.append([
            InlineKeyboardButton(
                text=f"#{order.id} — {status_text}",
                callback_data=f"order_info_{order.id}"
            )
        ])
        if order.status in ACTIVE_STATUSES:
            buttons.append([
                InlineKeyboardButton(
                    text="🚫 Отменить эту заявку",
                    callback_data=f"cancel_order_{order.id}"
                )
            ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def confirm_cancel_keyboard(order_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Да, отменить",
                    callback_data=f"confirm_cancel_{order_id}"
                ),
                InlineKeyboardButton(
                    text="◀️ Назад",
                    callback_data="back_to_orders"
                ),
            ]
        ]
    )


async def get_active_orders(telegram_id: int, db_session):
    """
    Возвращает только активные заявки клиента.
    Отменённые и выполненные не показываем.
    """
    order_service = OrderService(db_session)
    all_orders = await order_service.get_client_orders(telegram_id=telegram_id)
    return [order for order in all_orders if order.status in ACTIVE_STATUSES]


@router.message(Command("myorders"))
@router.message(F.text == "📂 Мои заявки")
async def cmd_myorders(message: Message, db_session):
    orders = await get_active_orders(message.from_user.id, db_session)

    if not orders:
        await message.answer(
            "У вас нет активных заявок.\n\n"
            "Нажмите 📋 Создать заявку чтобы оставить новую.",
            reply_markup=main_menu_keyboard()
        )
        return

    await message.answer(
        f"📂 Ваши активные заявки ({len(orders)} шт.):\n\n"
        "Нажмите 🚫 чтобы отменить заявку.",
        reply_markup=orders_list_keyboard(orders)
    )


@router.callback_query(F.data.startswith("order_info_"))
async def order_info(callback: CallbackQuery, db_session):
    order_id = int(callback.data.split("_")[-1])
    order_service = OrderService(db_session)
    order = await order_service.get_order_by_id(order_id)

    if not order:
        await callback.answer("Заявка не найдена.", show_alert=True)
        return

    status_text = STATUS_EMOJI.get(order.status, order.status)
    await callback.answer(
        f"Заявка #{order.id}\n"
        f"Статус: {status_text}\n\n"
        f"{order.description}",
        show_alert=True
    )


@router.callback_query(F.data.startswith("cancel_order_"))
async def cancel_order_request(callback: CallbackQuery):
    order_id = int(callback.data.split("_")[-1])
    await callback.message.edit_text(
        f"Вы уверены что хотите отменить заявку #{order_id}?",
        reply_markup=confirm_cancel_keyboard(order_id)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("confirm_cancel_"))
async def confirm_cancel_order(callback: CallbackQuery, db_session):
    order_id = int(callback.data.split("_")[-1])
    order_service = OrderService(db_session)
    order = await order_service.cancel_order_by_client(order_id)

    if not order:
        await callback.answer("Заявка не найдена.", show_alert=True)
        return

    # После отмены показываем обновлённый список активных заявок
    orders = await get_active_orders(callback.from_user.id, db_session)

    if not orders:
        await callback.message.edit_text(
            "✅ Заявка успешно отменена.\n\n"
            "У вас больше нет активных заявок."
        )
    else:
        await callback.message.edit_text(
            f"✅ Заявка #{order_id} отменена.\n\n"
            f"📂 Ваши активные заявки ({len(orders)} шт.):",
            reply_markup=orders_list_keyboard(orders)
        )
    await callback.answer()


@router.callback_query(F.data == "back_to_orders")
async def back_to_orders(callback: CallbackQuery, db_session):
    orders = await get_active_orders(callback.from_user.id, db_session)

    if not orders:
        await callback.message.edit_text(
            "У вас нет активных заявок.\n\n"
            "Нажмите 📋 Создать заявку чтобы оставить новую."
        )
    else:
        await callback.message.edit_text(
            f"📂 Ваши активные заявки ({len(orders)} шт.):\n\n"
            "Нажмите 🚫 чтобы отменить заявку.",
            reply_markup=orders_list_keyboard(orders)
        )
    await callback.answer()