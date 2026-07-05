from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from app.services.order_service import OrderService
from app.services.notification_service import NotificationService
from app.models.order import OrderStatus
from config.settings import settings

router = Router()


def is_admin(telegram_id: int) -> bool:
    return telegram_id in settings.admin_ids


@router.callback_query(F.data.startswith("admin_accept_"))
async def admin_accept_order(callback: CallbackQuery, db_session, bot: Bot):
    if not is_admin(callback.from_user.id):
        await callback.answer("У вас нет прав.", show_alert=True)
        return

    order_id = int(callback.data.split("_")[-1])
    order_service = OrderService(db_session)
    order = await order_service.get_order_by_id(order_id)

    if not order:
        await callback.answer("Заявка не найдена.", show_alert=True)
        return

    if order.status != OrderStatus.new:
        await callback.answer("Заявка уже обработана.", show_alert=True)
        return

    await order_service.update_order_status(order_id, OrderStatus.in_progress)

    # Убираем кнопки, обновляем сообщение
    await callback.message.edit_text(
        callback.message.text + "\n\n✅ Принята в работу",
        reply_markup=None
    )

    # Уведомляем клиента
    notification_service = NotificationService(bot)
    await notification_service.notify_client(
        telegram_id=order.client.telegram_id,
        order_id=order_id,
        status="in_progress",
    )

    await callback.answer("Заявка принята в работу.")


@router.callback_query(F.data.startswith("admin_reject_"))
async def admin_reject_order(callback: CallbackQuery, db_session, bot: Bot):
    if not is_admin(callback.from_user.id):
        await callback.answer("У вас нет прав.", show_alert=True)
        return

    order_id = int(callback.data.split("_")[-1])
    order_service = OrderService(db_session)
    order = await order_service.get_order_by_id(order_id)

    if not order:
        await callback.answer("Заявка не найдена.", show_alert=True)
        return

    if order.status != OrderStatus.new:
        await callback.answer("Заявка уже обработана.", show_alert=True)
        return

    await order_service.update_order_status(order_id, OrderStatus.cancelled)

    # Убираем кнопки, обновляем сообщение
    await callback.message.edit_text(
        callback.message.text + "\n\n❌ Отклонена",
        reply_markup=None
    )

    # Уведомляем клиента
    notification_service = NotificationService(bot)
    await notification_service.notify_client(
        telegram_id=order.client.telegram_id,
        order_id=order_id,
        status="cancelled",
    )

    await callback.answer("Заявка отклонена.")