from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import OrderStatus
from app.repositories.client import ClientRepository
from app.repositories.order import OrderRepository


class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.order_repo = OrderRepository(session)
        self.client_repo = ClientRepository(session)

    async def create_order(
        self,
        telegram_id: int,
        description: str,
        username: str = None,
        first_name: str = None,
        last_name: str = None,
    ):
        client = await self.client_repo.get_or_create(
            telegram_id=telegram_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        order = await self.order_repo.create(
            client_id=client.id,
            description=description,
            status=OrderStatus.new,
        )
        return order

    async def get_client_orders(self, telegram_id: int):
        client = await self.client_repo.get_by_telegram_id(telegram_id)
        if not client:
            return []
        return await self.order_repo.get_by_client(client.id)

    async def get_order_by_id(self, order_id: int):
        return await self.order_repo.get_by_id(order_id)

    async def update_order_status(self, order_id: int, new_status: OrderStatus):
        return await self.order_repo.update_status(order_id, new_status)

    async def cancel_order_by_client(self, order_id: int):
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            return None
        if order.status in (OrderStatus.new, OrderStatus.in_progress):
            return await self.order_repo.update_status(order_id, OrderStatus.cancelled)
        return None