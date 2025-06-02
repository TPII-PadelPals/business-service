import uuid

from fastapi import APIRouter, Depends, status

from app.models.business import (
    BusinessCreate,
    BusinessesFilters,
    BusinessesPublic,
    BusinessPublic,
    BusinessUpdate,
)
from app.services.business_service import BusinessService
from app.utilities.dependencies import SessionDep
from app.utilities.messages import BUSINESS_CREATE, BUSINESS_UPDATE

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
    *,
    session: SessionDep,
    businesses_filters: BusinessesFilters = Depends(),
    skip: int = 0,
    limit: int = 100,
) -> BusinessesPublic:
    """
    Get all businesses, optionally filtered by owner_id and/or by business_public_id.
    With pagination using skip and limit parameters.
    """
    return await service.get_businesses(session, businesses_filters, skip, limit)


@router.patch(
    "/{business_public_id}",
    response_model=BusinessPublic,
    status_code=status.HTTP_200_OK,
    responses=BUSINESS_UPDATE,
)
async def modify_businesses(
    *,
    session: SessionDep,
    owner_id: uuid.UUID,
    business_public_id: uuid.UUID,
    business_in: BusinessUpdate,
) -> BusinessPublic:
    """
    Update business.
    """
    business = await service.update_business(
        session, owner_id, business_public_id, business_in
    )
    return business
