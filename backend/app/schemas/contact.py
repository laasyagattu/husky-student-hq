from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.coffee_chat import CoffeeChatRead


class ContactBase(BaseModel):
    name: str
    company_id: int | None = None
    title: str | None = None
    email: str | None = None
    linkedin_url: str | None = None
    how_met: str | None = None
    notes: str | None = None


class ContactCreate(ContactBase):
    pass


class ContactUpdate(BaseModel):
    name: str | None = None
    company_id: int | None = None
    title: str | None = None
    email: str | None = None
    linkedin_url: str | None = None
    how_met: str | None = None
    notes: str | None = None


class ContactRead(ContactBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ContactDetail(ContactRead):
    coffee_chats: list[CoffeeChatRead] = []