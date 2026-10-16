from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.company import Company


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(primary_key=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"), index=True
    )
    role: Mapped[str] = mapped_column(String(200))
    posting_url: Mapped[str | None] = mapped_column(String(1000))
    job_description: Mapped[str | None] = mapped_column(Text)
    date_posted: Mapped[date | None] = mapped_column(Date)
    date_applied: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(50), server_default="saved")
    resume_version: Mapped[str | None] = mapped_column(String(200))
    cover_letter: Mapped[str | None] = mapped_column(String(200))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    company: Mapped["Company"] = relationship(back_populates="applications")
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )