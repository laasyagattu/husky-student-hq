from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.coffee_chat import CoffeeChat
from app.schemas.coffee_chat import CoffeeChatCreate, CoffeeChatUpdate

CLOSED_STATUSES = ("completed", "declined")


def get_coffee_chats(
    db: Session, contact_id: int | None = None, status: str | None = None
) -> list[CoffeeChat]:
    query = select(CoffeeChat).order_by(CoffeeChat.created_at.desc())
    if contact_id is not None:
        query = query.where(CoffeeChat.contact_id == contact_id)
    if status is not None:
        query = query.where(CoffeeChat.status == status)
    return list(db.scalars(query))


def get_due_follow_ups(db: Session) -> list[CoffeeChat]:
    query = (
        select(CoffeeChat)
        .where(CoffeeChat.follow_up_date <= date.today())
        .where(CoffeeChat.status.not_in(CLOSED_STATUSES))
        .order_by(CoffeeChat.follow_up_date)
    )
    return list(db.scalars(query))


def get_coffee_chat(db: Session, chat_id: int) -> CoffeeChat | None:
    return db.get(CoffeeChat, chat_id)


def create_coffee_chat(db: Session, data: CoffeeChatCreate) -> CoffeeChat:
    chat = CoffeeChat(**data.model_dump())
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat


def update_coffee_chat(
    db: Session, chat: CoffeeChat, data: CoffeeChatUpdate
) -> CoffeeChat:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(chat, field, value)
    db.commit()
    db.refresh(chat)
    return chat


def delete_coffee_chat(db: Session, chat: CoffeeChat) -> None:
    db.delete(chat)
    db.commit()