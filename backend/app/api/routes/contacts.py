from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import company as company_crud
from app.crud import contact as crud
from app.db.session import get_db
from app.schemas.contact import ContactCreate, ContactDetail, ContactRead, ContactUpdate

router = APIRouter(prefix="/contacts", tags=["contacts"])


def get_contact_or_404(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.get_contact(db, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


def check_company_exists(db: Session, company_id: int | None) -> None:
    if company_id is not None and company_crud.get_company(db, company_id) is None:
        raise HTTPException(status_code=404, detail="Company not found")


@router.get("", response_model=list[ContactRead])
def list_contacts(company_id: int | None = None, db: Session = Depends(get_db)):
    return crud.get_contacts(db, company_id=company_id)


@router.post("", response_model=ContactRead, status_code=status.HTTP_201_CREATED)
def create_contact(data: ContactCreate, db: Session = Depends(get_db)):
    check_company_exists(db, data.company_id)
    return crud.create_contact(db, data)


@router.get("/{contact_id}", response_model=ContactDetail)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.get_contact_detail(db, contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.patch("/{contact_id}", response_model=ContactRead)
def update_contact(
    data: ContactUpdate,
    contact=Depends(get_contact_or_404),
    db: Session = Depends(get_db),
):
    check_company_exists(db, data.company_id)
    return crud.update_contact(db, contact, data)


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_contact(contact=Depends(get_contact_or_404), db: Session = Depends(get_db)):
    crud.delete_contact(db, contact)