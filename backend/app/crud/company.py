from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload

from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate


def get_companies(db: Session) -> list[Company]:
    return list(db.scalars(select(Company).order_by(Company.name)))


def get_company(db: Session, company_id: int) -> Company | None:
    return db.get(Company, company_id)


def create_company(db: Session, data: CompanyCreate) -> Company:
    company = Company(**data.model_dump())
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def update_company(db: Session, company: Company, data: CompanyUpdate) -> Company:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(company, field, value)
    db.commit()
    db.refresh(company)
    return company


def delete_company(db: Session, company: Company) -> None:
    db.delete(company)
    db.commit()


def get_company_detail(db: Session, company_id: int) -> Company | None:
    query = (
        select(Company)
        .options(selectinload(Company.applications), selectinload(Company.contacts))
        .where(Company.id == company_id)
    )
    return db.scalar(query)