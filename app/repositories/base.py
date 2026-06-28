from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class BaseRepository:
    def __init__(self, session: AsyncSession, model):
        self.session = session
        self.model = model

    async def get_by_id(self, id: int):
        result = await self.session.get(self.model, id)
        return result

    async def get_all(self):
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def create(self, **kwargs):
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, id: int):
        obj = await self.get_by_id(id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
        return obj