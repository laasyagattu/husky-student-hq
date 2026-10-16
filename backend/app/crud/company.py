from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload

from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyUpdate


def get_companies(db: Session, user_id: int) -> list[Company]:
    query = select(Company).where(Company.user_id == user_id).order_by(Company.name)
    return list(db.scalars(query))


def get_company(db: Session, company_id: int, user_id: int) -> Company | None:
    company = db.get(Company, company_id)
    if company is None or company.user_id != user_id:
        return None
    return company


def create_company(db: Session, data: CompanyCreate, user_id: int) -> Company:
    company = Company(**data.model_dump(), user_id = user_id)
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


def get_company_detail(db: Session, company_id: int, user_id: int) -> Company | None:
    query = (
        select(Company)
        .options(selectinload(Company.applications), selectinload(Company.contacts))
        .where(Company.id == company_id, Company.user_id == user_id)
    )
    return db.scalar(query)