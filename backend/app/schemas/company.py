from datetime import datetime
from pydantic import BaseModel, ConfigDict
from app.schemas.application import ApplicationRead


class CompanyBase(BaseModel):
    name: str
    website: str | None = None
    notes: str | None = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    # every field optional, so you can update just one
    name: str | None = None
    website: str | None = None
    notes: str | None = None


class CompanyRead(CompanyBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CompanyDetail(CompanyRead):
    applications: list[ApplicationRead] = []