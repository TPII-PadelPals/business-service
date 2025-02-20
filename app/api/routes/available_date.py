import uuid
from typing import Any

from fastapi import APIRouter, Depends, status

from datetime import date
from app.models.available_date import AvailableDatePublic, AvailableDateCreate, AvailableDatesPublic
from app.utilities.dependencies import SessionDep, get_user_id_param
from app.utilities.messages import ITEM_RESPONSES, NOT_ENOUGH_PERMISSIONS

router = APIRouter()


@router.post(
    "/",
    response_model=AvailableDatePublic,
    status_code=status.HTTP_201_CREATED,
    responses={**NOT_ENOUGH_PERMISSIONS},  # type: ignore[dict-item]
    dependencies=[Depends(get_user_id_param)],
)
async def add_available_date(
        *,
        session: SessionDep,
        user_id: uuid.UUID,
        court_id: uuid.UUID,
        available_date_in: AvailableDateCreate
) -> Any:
    """
    Create new item.
    """
    return


@router.delete(
    "/",
    response_model=AvailableDatePublic,
    status_code=status.HTTP_201_CREATED,
    responses={**NOT_ENOUGH_PERMISSIONS},  # type: ignore[dict-item]
    dependencies=[Depends(get_user_id_param)],
)
async def delete_available_date(
        *,
        session: SessionDep,
        user_id: uuid.UUID,
        court_id: uuid.UUID,
        available_date_in: AvailableDateCreate
) -> Any:
    """
    Delete a item.
    """
    return


@router.put(
    "/",
    response_model=AvailableDatePublic,
    status_code=status.HTTP_200_OK,
    responses={**ITEM_RESPONSES},  # type: ignore[dict-item]
    dependencies=[Depends(get_user_id_param)],
)
async def modify_available_date(
        *,
        session: SessionDep,
        user_id: uuid.UUID,
        court_id: uuid.UUID,
        available_date_in: AvailableDateCreate
) -> Any:
    """
    Update an item.
    """
    return


@router.get(
    "/",
    response_model=AvailableDatesPublic,
    status_code=status.HTTP_200_OK,
    responses={**ITEM_RESPONSES},  # type: ignore[dict-item]
    dependencies=[Depends(get_user_id_param)],
)
async def get_available_dates(
        *,
        session: SessionDep,
        court_id: uuid.UUID,
        date: date,
) -> Any:
    """
    Get all item.
    """
    return


@router.patch(
    "/",
    response_model=AvailableDatePublic,
    status_code=status.HTTP_200_OK,
    responses={**ITEM_RESPONSES},  # type: ignore[dict-item]
    dependencies=[Depends(get_user_id_param)],
)
async def reserve_available_date(
        *,
        session: SessionDep,
        court_id: uuid.UUID,
        date: date,
        hour: int,
) -> Any:
    """
    Update an item.
    """
    return
