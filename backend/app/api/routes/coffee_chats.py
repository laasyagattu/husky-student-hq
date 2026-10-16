from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import coffee_chat as crud
from app.crud import contact as contact_crud
from app.db.session import get_db
from app.schemas.coffee_chat import (
    CoffeeChatCreate,
    CoffeeChatRead,
    CoffeeChatStatus,
    CoffeeChatUpdate,
)
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/coffee-chats", tags=["coffee chats"])


def get_chat_or_404(chat_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    chat = crud.get_coffee_chat(db, chat_id, user.id)
    if chat is None:
        raise HTTPException(status_code=404, detail="Coffee chat not found")
    return chat


@router.get("", response_model=list[CoffeeChatRead])
def list_coffee_chats(
    contact_id: int | None = None,
    status: CoffeeChatStatus | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return crud.get_coffee_chats(db, user.id, contact_id=contact_id, status=status)


# must come before /{chat_id}, or FastAPI tries to read "follow-ups" as an id
@router.get("/follow-ups", response_model=list[CoffeeChatRead])
def list_due_follow_ups(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return crud.get_due_follow_ups(db)


@router.post("", response_model=CoffeeChatRead, status_code=status.HTTP_201_CREATED)
def create_coffee_chat(data: CoffeeChatCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if contact_crud.get_contact(db, data.contact_id, user.id) is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return crud.create_coffee_chat(db, data, user.id)


@router.get("/{chat_id}", response_model=CoffeeChatRead)
def read_coffee_chat(chat=Depends(get_chat_or_404)):
    return chat


@router.patch("/{chat_id}", response_model=CoffeeChatRead)
def update_coffee_chat(
    data: CoffeeChatUpdate,
    chat=Depends(get_chat_or_404),
    db: Session = Depends(get_db),
):
    return crud.update_coffee_chat(db, chat, data)


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_coffee_chat(chat=Depends(get_chat_or_404), db: Session = Depends(get_db)):
    crud.delete_coffee_chat(db, chat)