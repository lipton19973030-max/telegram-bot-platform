from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger

from config.settings import settings


class NotificationService:
    def __init__(self, bot: Bot):
        self.bot = bot

    def _admin_order_keyboard(self, order_id: int) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Принять",
                        callback_data=f"admin_accept_{order_id}"
                    ),
                    InlineKeyboardButton(
                        text="❌ Отклонить",
                        callback_data=f"admin_reject_{order_id}"
                    ),
                ]
            ]
        )

    async def notify_admins_new_order(
        self,
        order_id: int,
        service: str,
        description: str,
        client_name: str,
        client_username: str | None,
        telegram_id: int,
    ) -> None:
        username_text = f"@{client_username}" if client_username else "нет username"
        message_text = (
            f"🆕 Новая заявка #{order_id}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 Клиент: {client_name} ({username_text})\n"
            f"🆔 Telegram ID: {telegram_id}\n"
            f"🔧 Услуга: {service}\n"
            f"📝 Описание:\n{description}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📌 Статус: Новая"
        )

        for admin_id in settings.admin_ids:
            try:
                await self.bot.send_message(
                    chat_id=admin_id,
                    text=message_text,
                    reply_markup=self._admin_order_keyboard(order_id),
                )
                logger.info(f"Уведомление о заявке #{order_id} отправлено админу {admin_id}")
            except Exception as error:
                logger.error(f"Не удалось отправить уведомление админу {admin_id}: {error}")

    async def notify_client(
        self,
        telegram_id: int,
        order_id: int,
        status: str,
    ) -> None:
        status_messages = {
            "in_progress": f"⚙️ Ваша заявка #{order_id} принята в работу!\n\nМы свяжемся с вами в ближайшее время.",
            "cancelled": f"❌ Ваша заявка #{order_id} была отклонена.\n\nЕсли это ошибка — создайте новую заявку или напишите @adm_uslugi_andrey.",
        }
        text = status_messages.get(status)
        if not text:
            return

        try:
            await self.bot.send_message(chat_id=telegram_id, text=text)
            logger.info(f"Уведомление клиенту {telegram_id} о заявке #{order_id} отправлено")
        except Exception as error:
            logger.error(f"Не удалось отправить уведомление клиенту {telegram_id}: {error}")