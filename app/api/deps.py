from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.registration_service import RegistrationService


def get_registration_service(
    session: Session = Depends(get_db),
) -> RegistrationService:
    return RegistrationService(session)
