import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from app.models.padel_court import (
    PadelCourtCreate,
    PadelCourtFilter,
    PadelCourtPublic,
    PadelCourtUpdate,
)
from app.models.padel_court_extended import PadelCourtsPublicExtended
from app.repository.padel_court_repository import PadelCourtRepository
from app.services.court_extended_service import PadelCourtExtendedService
from app.services.court_owner_verification_service import CourtOwnerVerificationService
from app.services.padel_court_service import PadelCourtService
from app.utilities.dependencies import SessionDep, get_business_public_id_param
from app.utilities.exceptions import (
    BusinessNotFoundException,
    BusinessNotFoundHTTPException,
    NotEnoughPermissionsException,
    UnauthorizedPadelCourtOperationException,
)
from app.utilities.messages import BUSINESS_RESPONSES, COURT_UPDATE

router = APIRouter()

service = PadelCourtService()


@router.post(
    "/",
    response_model=PadelCourtPublic,
    status_code=status.HTTP_201_CREATED,
    responses={**BUSINESS_RESPONSES},  # type: ignore[dict-item]
    dependencies=[Depends(get_business_public_id_param)],
)
async def create_padel_court(
    *,
    session: SessionDep,
    owner_id: uuid.UUID,
    business_public_id: uuid.UUID,
    padel_court_in: PadelCourtCreate,
) -> PadelCourtPublic:
    """
    Create new Padel Court.
    """
    try:
        repo = PadelCourtRepository(session)
        padel_court = await repo.create_padel_court(
            owner_id, business_public_id, padel_court_in
        )
        return PadelCourtPublic.from_private(padel_court)
    except BusinessNotFoundException as e:
        raise BusinessNotFoundHTTPException(error_message=str(e))
    except UnauthorizedPadelCourtOperationException:
        raise NotEnoughPermissionsException()


@router.get("/", response_model=PadelCourtsPublicExtended)
async def read_padel_courts(
    *,
    session: SessionDep,
    user_id: uuid.UUID = None,
    skip: int = 0,
    limit: int = 100,
    court_filters: PadelCourtFilter = Depends(),
) -> PadelCourtsPublicExtended:
    """
    Get all padel courts, optionally filtered by business_public_id.
    With pagination using skip and limit parameters.
    """
    if court_filters.is_valid_filter_for_business_public_id(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both business_public_id and user_id must be provided together or both omitted.",
        )

    public_courts = await service.get_padel_courts(
        session, user_id, skip, limit, court_filters
    )
    return await PadelCourtExtendedService().get_public_courts_extended(
        session, public_courts
    )


@router.patch(
    "/{court_public_id}",
    response_model=PadelCourtPublic,
    status_code=status.HTTP_200_OK,
    responses={**COURT_UPDATE},
)
async def modify_court(
    *,
    session: SessionDep,
    business_public_id: uuid.UUID,
    court_public_id: uuid.UUID,
    user_id: uuid.UUID,
    court_in: PadelCourtUpdate,
) -> PadelCourtPublic:
    """
    Update padel court.
    """
    service_aux = CourtOwnerVerificationService()
    await service_aux.verification_of_court_owner_without_name(
        session, user_id, business_public_id, court_public_id
    )
    court = await service.update_padel_court(session, court_public_id, court_in)
    return court
