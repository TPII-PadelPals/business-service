import uuid
from datetime import date
from typing import Any

from fastapi import APIRouter, status

from app.models.available_date import (
    AvailableDateCreate,
    AvailableDatePublic,
    AvailableDatesPublic,
)
from app.services.available_date import AvailableDateService
from app.utilities.dependencies import SessionDep
from app.utilities.messages import ITEM_RESPONSES, NOT_ENOUGH_PERMISSIONS

router = APIRouter()

service = AvailableDateService()


@router.post(
    "/",
    response_model=AvailableDatesPublic,
    status_code=status.HTTP_201_CREATED,
    responses={**NOT_ENOUGH_PERMISSIONS},  # type: ignore[dict-item]
)
async def add_available_date(
    *,
    session: SessionDep,
    user_id: uuid.UUID,
    court_name: str,
    business_id: uuid.UUID,
    available_date_in: AvailableDateCreate,
) -> Any:
    """
    Create new available date, enabling games on the date.
    """
    available_dates = await service.create_available_date(
        session, user_id, court_name, business_id, available_date_in
    )
    return AvailableDatesPublic.from_private(available_dates)


@router.delete(
    "/",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    responses={**NOT_ENOUGH_PERMISSIONS},  # type: ignore[dict-item]
)
async def delete_available_date(
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
    await service.delete_available_date(session, user_id, court_name, business_id, date)
    return


@router.get(
    "/",
    response_model=AvailableDatesPublic,
    status_code=status.HTTP_200_OK,
    responses={**ITEM_RESPONSES},  # type: ignore[dict-item]
)
async def get_available_dates(
    *,
    session: SessionDep,
    court_name: str,
    business_id: uuid.UUID,
    date: date,
) -> Any:
    """
    Get all item.
    """
    available_dates = await service.get_available_date(
        session, court_name, business_id, date
    )
    return AvailableDatesPublic.from_private(available_dates)


@router.patch(
    "/",
    response_model=AvailableDatePublic,
    status_code=status.HTTP_200_OK,
    responses={**ITEM_RESPONSES},  # type: ignore[dict-item]
)
async def reserve_available_date(
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
    available_date = await service.update_for_reserve_available_date(
        session, court_name, business_id, date, hour
    )
    return AvailableDatePublic.from_private(available_date)
