from fastapi import APIRouter, status

from app.models.owner import OwnerCreate, OwnerPublic
from app.services.owner_service import OwnerService
from app.utilities.dependencies import SessionDep
from app.utilities.messages import CREATE_OWNER

router = APIRouter()

service = OwnerService()


@router.post(
    "/",
    response_model=OwnerPublic,
    status_code=status.HTTP_201_CREATED,
    responses={**CREATE_OWNER},  # type: ignore[dict-item]
)
async def create_business(*, session: SessionDep, owner_in: OwnerCreate) -> OwnerPublic:
    """
    Create a new Owner.
    """
    owner = await service.create_owner(session, owner_in)
    return OwnerPublic.from_public(owner)
