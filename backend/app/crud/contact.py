from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate


def get_contacts(db: Session, user_id: int, company_id: int | None = None) -> list[Contact]:
    query = select(Contact).where(Contact.user_id == user_id).order_by(Contact.name)
    if company_id is not None:
        query = query.where(Contact.company_id == company_id)
    return list(db.scalars(query))


def get_contact(db: Session, contact_id: int, user_id: int) -> Contact | None:
    contact = db.get(Contact, contact_id)
    if contact is None or contact.user_id != user_id:
        return None
    return contact


def get_contact_detail(db: Session, contact_id: int, user_id: int) -> Contact | None:
    query = (
        select(Contact)
        .options(selectinload(Contact.coffee_chats))
        .where(Contact.id == contact_id, Contact.user_id == user_id)
    )
    return db.scalar(query)


def create_contact(db: Session, data: ContactCreate, user_id: int) -> Contact:
    contact = Contact(**data.model_dump(), user_id = user_id)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


def update_contact(db: Session, contact: Contact, data: ContactUpdate) -> Contact:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(contact, field, value)
    db.commit()
    db.refresh(contact)
    return contact


def delete_contact(db: Session, contact: Contact) -> None:
    db.delete(contact)
    db.commit()