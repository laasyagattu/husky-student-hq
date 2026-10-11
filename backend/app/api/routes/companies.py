from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.crud import company as crud
from app.db.session import get_db
from app.schemas.company import CompanyCreate, CompanyDetail, CompanyRead, CompanyUpdate

router = APIRouter(prefix="/companies", tags=["companies"])


def get_company_or_404(company_id: int, db: Session = Depends(get_db)):
    company = crud.get_company(db, company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.get("", response_model=list[CompanyRead])
def list_companies(db: Session = Depends(get_db)):
    return crud.get_companies(db)


@router.post("", response_model=CompanyRead, status_code=status.HTTP_201_CREATED)
def create_company(data: CompanyCreate, db: Session = Depends(get_db)):
    return crud.create_company(db, data)


@router.get("/{company_id}", response_model=CompanyDetail)
def read_company(company_id: int, db: Session = Depends(get_db)):
    company = crud.get_company_with_applications(db, company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@router.patch("/{company_id}", response_model=CompanyRead)
def update_company(
    data: CompanyUpdate,
    company=Depends(get_company_or_404),
    db: Session = Depends(get_db),
):
    return crud.update_company(db, company, data)


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company=Depends(get_company_or_404), db: Session = Depends(get_db)):
    crud.delete_company(db, company)