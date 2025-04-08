import uuid
from datetime import date
from typing import Any

from fastapi import APIRouter, status

from app.models.available_match import (
    AvailableMatchCreate,
    AvailableMatchesPublic,
    AvailableMatchPublic,
)
from app.services.available_match_service import AvailableMatchService
from app.services.business_service import BusinessService
from app.utilities.dependencies import SessionDep
from app.utilities.messages import (
    AVAILABLE_DATE_DELETE_RESPONSES,
    AVAILABLE_DATE_GET_RESPONSES,
    AVAILABLE_DATE_PATCH_RESPONSES,
    AVAILABLE_DATE_POST_RESPONSES,
)

router = APIRouter()

service = AvailableMatchService()
business_service = BusinessService()


@router.post(
    "/",
    response_model=AvailableMatchesPublic,
    status_code=status.HTTP_201_CREATED,
    responses={**AVAILABLE_DATE_POST_RESPONSES},  # type: ignore[dict-item]
)
async def add_available_matches_in_date(
    *,
    session: SessionDep,
    user_id: uuid.UUID,
    court_name: str,
    business_public_id: uuid.UUID,
    available_match_in: AvailableMatchCreate,
) -> Any:
    """
    Create new available date, enabling games on the date.
    """
    available_matches = await service.create_available_matches_in_date(
        session, user_id, court_name, business_public_id, available_match_in
    )
    business = await business_service.get_business(session, business_public_id)
    return AvailableMatchesPublic.from_private(
        available_matches, business.get_coordinates()
    )


@router.delete(
    "/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={**AVAILABLE_DATE_DELETE_RESPONSES},  # type: ignore[dict-item]
)
async def delete_available_matches_in_date(
    *,
    session: SessionDep,
    user_id: uuid.UUID,
    court_name: str,
    business_public_id: uuid.UUID,
    date: date,
) -> Any:
    """
    Delete a item.
    """
    await service.delete_available_matches_in_date(
        session, user_id, court_name, business_public_id, date
    )
    return


@router.get(
    "/",
    response_model=AvailableMatchesPublic,
    status_code=status.HTTP_200_OK,
    responses={**AVAILABLE_DATE_GET_RESPONSES},  # type: ignore[dict-item]
)
async def get_available_matches_in_date(
    *,
    session: SessionDep,
    court_name: str,
    business_public_id: uuid.UUID,
    date: date,
) -> Any:
    """
    Get all item.
    """
    available_matches = await service.get_available_matches_in_date(
        session, court_name, business_public_id, date
    )
    business = await business_service.get_business(session, business_public_id)
    return AvailableMatchesPublic.from_private(
        available_matches, business.get_coordinates()
    )


@router.patch(
    "/",
    response_model=AvailableMatchPublic,
    status_code=status.HTTP_200_OK,
    responses={**AVAILABLE_DATE_PATCH_RESPONSES},  # type: ignore[dict-item]
)
async def reserve_available_match(
    *,
    session: SessionDep,
    court_name: str,
    business_public_id: uuid.UUID,
    date: date,
    hour: int,
) -> Any:
    """
    Update an item.
    """
    available_match = await service.reserve_available_match(
        session, court_name, business_public_id, date, hour
    )
    business = await business_service.get_business(session, business_public_id)
    return AvailableMatchPublic.from_private(
        available_match, business.get_coordinates()
    )
