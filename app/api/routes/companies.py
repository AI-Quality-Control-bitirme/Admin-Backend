from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_registration_service
from app.schemas.company import CompanyRead, CompanyRegister, CompanyRegistrationRead
from app.schemas.user import UserRead
from app.services.errors import ConflictError
from app.services.registration_service import RegistrationService

router = APIRouter(prefix="/companies", tags=["companies"])


@router.post(
    "/register",
    response_model=CompanyRegistrationRead,
    status_code=status.HTTP_201_CREATED,
)
def register_company(
    data: CompanyRegister,
    service: RegistrationService = Depends(get_registration_service),
) -> CompanyRegistrationRead:
    try:
        company, admin = service.register_company(data)
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return CompanyRegistrationRead(
        company=CompanyRead.model_validate(company),
        admin=UserRead.model_validate(admin),
    )
