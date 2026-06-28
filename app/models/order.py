from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum
from app.database.base import Base, TimestampMixin
import enum


class OrderStatus(enum.Enum):
    new = "new"
    in_progress = "in_progress"
    completed = "completed"
    cancelled = "cancelled"


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    bot_id = Column(Integer, ForeignKey("bots.id"), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.new)
    description = Column(Text, nullable=True)
    contact_phone = Column(String, nullable=True)