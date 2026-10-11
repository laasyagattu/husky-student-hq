from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

CoffeeChatStatus = Literal[
    "reached_out", "replied", "scheduled", "completed", "declined", "no_response"
]
OutreachChannel = Literal["linkedin", "email", "in_person", "other"]


class CoffeeChatBase(BaseModel):
    status: CoffeeChatStatus = "reached_out"
    outreach_channel: OutreachChannel | None = None
    outreach_date: date | None = None
    meeting_time: datetime | None = None
    follow_up_date: date | None = None
    notes: str | None = None


class CoffeeChatCreate(CoffeeChatBase):
    contact_id: int


class CoffeeChatUpdate(BaseModel):
    status: CoffeeChatStatus | None = None
    outreach_channel: OutreachChannel | None = None
    outreach_date: date | None = None
    meeting_time: datetime | None = None
    follow_up_date: date | None = None
    notes: str | None = None


class CoffeeChatRead(CoffeeChatBase):
    id: int
    contact_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)