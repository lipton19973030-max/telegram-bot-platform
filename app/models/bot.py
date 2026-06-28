from sqlalchemy import Column, Integer, String, Boolean, JSON
from app.database.base import Base, TimestampMixin


class Bot(Base, TimestampMixin):
    __tablename__ = "bots"

    id = Column(Integer, primary_key=True)
    token = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    is_active = Column(Boolean, default=True)
    config = Column(JSON, default=dict)