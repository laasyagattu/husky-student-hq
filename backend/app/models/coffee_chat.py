from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.contact import Contact


class CoffeeChat(Base):
    __tablename__ = "coffee_chats"

    id: Mapped[int] = mapped_column(primary_key=True)
    contact_id: Mapped[int] = mapped_column(
        ForeignKey("contacts.id", ondelete="CASCADE"), index=True
    )
    status: Mapped[str] = mapped_column(String(50), server_default="reached_out")
    outreach_channel: Mapped[str | None] = mapped_column(String(50))
    outreach_date: Mapped[date | None] = mapped_column(Date)
    meeting_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    follow_up_date: Mapped[date | None] = mapped_column(Date, index=True)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    contact: Mapped["Contact"] = relationship(back_populates="coffee_chats")