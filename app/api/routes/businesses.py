import uuid

from fastapi import APIRouter, status

from app.models.business import BusinessCreate, BusinessesPublic, BusinessPublic
from app.services.business_service import BusinessService
from app.utilities.dependencies import SessionDep
from app.utilities.messages import BUSINESS_CREATE

router = APIRouter()

service = BusinessService()


@router.post(
    "/",
    response_model=BusinessPublic,
    status_code=status.HTTP_201_CREATED,
    responses=BUSINESS_CREATE,
)
async def create_business(
    *, session: SessionDep, owner_id: uuid.UUID, business_in: BusinessCreate
) -> BusinessPublic:
    """
    Create a new Business.
    """
    business = await service.create_business(session, owner_id, business_in)
    return business


@router.get("/", response_model=BusinessesPublic)
async def read_businesses(
    *, session: SessionDep, owner_id: uuid.UUID = None, skip: int = 0, limit: int = 100
) -> BusinessesPublic:
    """
    Get all businesses, optionally filtered by owner_id.
    With pagination using skip and limit parameters.
    """
    return await service.get_businesses(session, owner_id, skip, limit)
