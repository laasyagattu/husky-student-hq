from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import application as crud
from app.crud import company as company_crud
from app.db.session import get_db
from app.schemas.application import (
    ApplicationCreate,
    ApplicationRead,
    ApplicationStatus,
    ApplicationUpdate,
)
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/applications", tags=["applications"])


def get_application_or_404(application_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    application = crud.get_application(db, application_id, user_id)
    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")
    return application


@router.get("", response_model=list[ApplicationRead])
def list_applications(
    company_id: int | None = None,
    status: ApplicationStatus | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return crud.get_applications(db, user.id, company_id=company_id, status=status)


@router.post("", response_model=ApplicationRead, status_code=status.HTTP_201_CREATED)
def create_application(data: ApplicationCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if company_crud.get_company(db, data.company_id) is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return crud.create_application(db, data)


@router.get("/{application_id}", response_model=ApplicationRead)
def read_application(application=Depends(get_application_or_404)):
    return application


@router.patch("/{application_id}", response_model=ApplicationRead)
def update_application(
    data: ApplicationUpdate,
    application=Depends(get_application_or_404),
    db: Session = Depends(get_db),
):
    return crud.update_application(db, application, data)


@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_application(
    application=Depends(get_application_or_404), db: Session = Depends(get_db)
):
    crud.delete_application(db, application)