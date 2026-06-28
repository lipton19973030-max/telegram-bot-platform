from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.repositories.base import BaseRepository
from app.models.order import Order, OrderStatus


class OrderRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Order)

    async def get_by_client(self, client_id: int):
        result = await self.session.execute(
            select(Order).where(Order.client_id == client_id)
        )
        return result.scalars().all()

    async def get_by_status(self, status: OrderStatus):
        result = await self.session.execute(
            select(Order).where(Order.status == status)
        )
        return result.scalars().all()

    async def update_status(self, order_id: int, status: OrderStatus):
        order = await self.get_by_id(order_id)
        if order:
            order.status = status
            await self.session.commit()
            await self.session.refresh(order)
        return order