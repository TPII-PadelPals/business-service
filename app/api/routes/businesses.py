import uuid

from fastapi import APIRouter, status

from app.models.business import BusinessCreate, BusinessPublic, BusinessesPublic
from app.repository.business_repository import BusinessRepository
from app.utilities.dependencies import SessionDep

router = APIRouter()


@router.post("/", response_model=BusinessPublic, status_code=status.HTTP_201_CREATED)
async def create_business(
    *, session: SessionDep, owner_id: uuid.UUID, business_in: BusinessCreate
) -> BusinessPublic:
    """
    Create a new Business.
    """
    repo = BusinessRepository(session)
    item = await repo.create_business(owner_id, business_in)
    return item


@router.get("/", response_model=BusinessesPublic)
async def read_businesses(
    *, session: SessionDep, owner_id: uuid.UUID = None, skip: int = 0, limit: int = 100
) -> BusinessesPublic:
    """
    Get all businesses, optionally filtered by owner_id.
    With pagination using skip and limit parameters.
    """
    repo = BusinessRepository(session)
    return await repo.get_businesses(owner_id, skip, limit)
