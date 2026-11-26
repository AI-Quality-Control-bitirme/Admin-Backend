import uuid
from datetime import datetime
from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, EmailStr, StringConstraints

from app.models.enums import UserRole


def _check_password(value: str) -> str:
    # bcrypt only uses the first 72 bytes of a password.
    if len(value.encode("utf-8")) > 72:
        raise ValueError("Password must be at most 72 bytes")
    return value


FullName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=120)]
Password = Annotated[str, StringConstraints(min_length=8), AfterValidator(_check_password)]
Email = Annotated[EmailStr, AfterValidator(str.lower)]


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    company_id: uuid.UUID | None
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime
