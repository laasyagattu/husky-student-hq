from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationUpdate


def get_applications(
    db: Session, company_id: int | None = None, status: str | None = None
) -> list[Application]:
    query = select(Application).order_by(Application.created_at.desc())
    if company_id is not None:
        query = query.where(Application.company_id == company_id)
    if status is not None:
        query = query.where(Application.status == status)
    return list(db.scalars(query))


def get_application(db: Session, application_id: int) -> Application | None:
    return db.get(Application, application_id)


def create_application(db: Session, data: ApplicationCreate) -> Application:
    application = Application(**data.model_dump())
    db.add(application)
    db.commit()
    db.refresh(application)
    return application


def update_application(
    db: Session, application: Application, data: ApplicationUpdate
) -> Application:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(application, field, value)
    db.commit()
    db.refresh(application)
    return application


def delete_application(db: Session, application: Application) -> None:
    db.delete(application)
    db.commit()