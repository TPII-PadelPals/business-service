import uuid
from datetime import date
from typing import Any

from fastapi import APIRouter, status

from app.models.available_match import (
    AvailableMatchCreate,
    AvailableMatchesPublic,
    AvailableMatchPublic,
)
from app.services.available_match_service import AvailableDateService
from app.utilities.dependencies import SessionDep
from app.utilities.messages import (
    AVAILABLE_DATE_DELETE_RESPONSES,
    AVAILABLE_DATE_GET_RESPONSES,
    AVAILABLE_DATE_PATCH_RESPONSES,
    AVAILABLE_DATE_POST_RESPONSES,
)

router = APIRouter()

service = AvailableDateService()


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
    business_id: uuid.UUID,
    available_match_in: AvailableMatchCreate,
) -> Any:
    """
    Create new available date, enabling games on the date.
    """
    available_matches = await service.create_available_matches_in_date(
        session, user_id, court_name, business_id, available_match_in
    )
    return AvailableMatchesPublic.from_private(available_matches)


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
    business_id: uuid.UUID,
    date: date,
) -> Any:
    """
    Delete a item.
    """
    await service.delete_available_matches_in_date(
        session, user_id, court_name, business_id, date
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
    business_id: uuid.UUID,
    date: date,
) -> Any:
    """
    Get all item.
    """
    available_matches = await service.get_available_matches_in_date(
        session, court_name, business_id, date
    )
    return AvailableMatchesPublic.from_private(available_matches)


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
    business_id: uuid.UUID,
    date: date,
    hour: int,
) -> Any:
    """
    Update an item.
    """
    available_match = await service.reserve_available_match(
        session, court_name, business_id, date, hour
    )
    return AvailableMatchPublic.from_private(available_match)
