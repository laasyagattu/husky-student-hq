from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

ApplicationStatus = Literal[
    "saved", "applied", "interviewing", "offer", "rejected", "withdrawn"
]


class ApplicationBase(BaseModel):
    role: str
    posting_url: str | None = None
    job_description: str | None = None
    date_posted: date | None = None
    date_applied: date | None = None
    status: ApplicationStatus = "saved"
    resume_version: str | None = None
    cover_letter: str | None = None


class ApplicationCreate(ApplicationBase):
    company_id: int


class ApplicationUpdate(BaseModel):
    role: str | None = None
    posting_url: str | None = None
    job_description: str | None = None
    date_posted: date | None = None
    date_applied: date | None = None
    status: ApplicationStatus | None = None
    resume_version: str | None = None
    cover_letter: str | None = None


class ApplicationRead(ApplicationBase):
    id: int
    company_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)