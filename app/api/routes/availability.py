import uuid
from typing import Any

from fastapi import APIRouter, Depends, status

from app.models.item import ItemCreate, ItemPublic, ItemsPublic, ItemUpdate
from app.models.message import Message
from app.repository.items_repository import ItemsRepository
from app.utilities.dependencies import SessionDep, get_user_id_param
from app.utilities.messages import ITEM_RESPONSES, NOT_ENOUGH_PERMISSIONS

router = APIRouter()


@router.post(
    "/",
    response_model=ItemPublic,
    status_code=status.HTTP_201_CREATED,
    responses={**NOT_ENOUGH_PERMISSIONS},  # type: ignore[dict-item]
    dependencies=[Depends(get_user_id_param)],
)
async def create_item(
        *, session: SessionDep, user_id: uuid.UUID, item_in: ItemCreate
) -> Any:
    """
    Create new item.
    """
    repo = ItemsRepository(session)
    item = await repo.create_item(user_id, item_in)
    return item


@router.patch(
    "/",
    response_model=ItemPublic,
    status_code=status.HTTP_200_OK,
    responses={**ITEM_RESPONSES},  # type: ignore[dict-item]
    dependencies=[Depends(get_user_id_param)],
)
async def update_item(
        *,
        session: SessionDep,
        user_id: uuid.UUID,
        id: uuid.UUID,
        item_in: ItemUpdate,
) -> Any:
    """
    Update an item.
    """
    repo = ItemsRepository(session)
    item = await repo.update_item(user_id, id, item_in)
    return item


@router.put(
    "/",
    response_model=ItemPublic,
    status_code=status.HTTP_200_OK,
    responses={**ITEM_RESPONSES},  # type: ignore[dict-item]
    dependencies=[Depends(get_user_id_param)],
)
async def update_item(
        *,
        session: SessionDep,
        user_id: uuid.UUID,
        id: uuid.UUID,
        item_in: ItemUpdate,
) -> Any:
    """
    Update an item.
    """
    repo = ItemsRepository(session)
    item = await repo.update_item(user_id, id, item_in)
    return item
