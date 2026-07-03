from aiogram import Bot
from loguru import logger

from config.settings import settings


class NotificationService:
    """
    Сервис отправки уведомлений администраторам.
    Отправляет сообщение всем администраторам из списка ADMIN_IDS.
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    async def notify_admins_new_order(
        self,
        order_id: int,
        service: str,
        description: str,
        client_name: str,
        client_username: str | None,
        telegram_id: int,
    ) -> None:
        """
        Отправляет уведомление о новой заявке всем администраторам.
        """
        username_text = f"@{client_username}" if client_username else "нет username"

        message_text = (
            f"🆕 <b>Новая заявка #{order_id}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 <b>Клиент:</b> {client_name} ({username_text})\n"
            f"🆔 <b>Telegram ID:</b> <code>{telegram_id}</code>\n"
            f"🔧 <b>Услуга:</b> {service}\n"
            f"📝 <b>Описание:</b> {description}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📌 Статус: <b>Новая</b>"
        )

        for admin_id in settings.admin_ids:
            try:
                await self.bot.send_message(
                    chat_id=admin_id,
                    text=message_text,
                    parse_mode="HTML",
                )
                logger.info(f"Уведомление о заявке #{order_id} отправлено админу {admin_id}")
            except Exception as error:
                logger.error(
                    f"Не удалось отправить уведомление админу {admin_id}: {error}"
                )