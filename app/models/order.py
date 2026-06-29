from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
import enum

from app.database.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.client import Client


class OrderStatus(str, enum.Enum):
    new = "new"
    in_progress = "in_progress"
    done = "done"
    cancelled = "cancelled"


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("clients.id"), nullable=False)
    bot_id: Mapped[int | None] = mapped_column(Integer, nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[OrderStatus] = mapped_column(
        default=OrderStatus.new, nullable=False
    )

    client: Mapped["Client"] = relationship("Client", back_populates="orders")