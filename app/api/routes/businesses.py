from typing import Any

from fastapi import APIRouter, status

from app.models.business import BusinessCreate, BusinessPublic
from app.repository.business_repository import BusinessRepository
from app.utilities.dependencies import SessionDep

router = APIRouter()


@router.post("/", response_model=BusinessPublic, status_code=status.HTTP_201_CREATED)
async def create_business(*, session: SessionDep, business_in: BusinessCreate) -> Any:
    """
    Create a new Business.
    """
    repo = BusinessRepository(session)
    item = await repo.create_business(business_in)
    return item
