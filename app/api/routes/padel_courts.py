import uuid

from fastapi import APIRouter, Depends, status

from app.models.padel_court import PadelCourtCreate, PadelCourtPublic
from app.repository.padel_court_repository import PadelCourtRepository
from app.utilities.dependencies import SessionDep, get_business_id_param
from app.utilities.messages import NOT_ENOUGH_PERMISSIONS

router = APIRouter()


@router.post(
    "/",
    response_model=PadelCourtPublic,
    status_code=status.HTTP_201_CREATED,
    responses={**NOT_ENOUGH_PERMISSIONS},  # type: ignore[dict-item]
    dependencies=[Depends(get_business_id_param)],
)
async def create_padel_court(
    *, session: SessionDep, business_id: uuid.UUID, padel_court_in: PadelCourtCreate
) -> PadelCourtPublic:
    """
    Create new Padel Court.
    """
    repo = PadelCourtRepository(session)
    padel_court = await repo.create_padel_court(business_id, padel_court_in)
    return padel_court
