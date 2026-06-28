from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.repositories.base import BaseRepository
from app.models.client import Client


class ClientRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Client)

    async def get_by_telegram_id(self, telegram_id: int):
        result = await self.session.execute(
            select(Client).where(Client.telegram_id == telegram_id)
        )
        return result.scalar_one_or_none()

    async def get_or_create(self, telegram_id: int, **kwargs):
        client = await self.get_by_telegram_id(telegram_id)
        if not client:
            client = await self.create(telegram_id=telegram_id, **kwargs)
        return client