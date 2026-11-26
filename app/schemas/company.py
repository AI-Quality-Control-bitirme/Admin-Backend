import uuid
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints

from app.schemas.user import Email, FullName, Password, UserRead

CompanyName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=120)]


class CompanyRegister(BaseModel):
    company_name: CompanyName
    admin_full_name: FullName
    admin_email: Email
    admin_password: Password


class CompanyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    created_at: datetime


class CompanyRegistrationRead(BaseModel):
    company: CompanyRead
    admin: UserRead
