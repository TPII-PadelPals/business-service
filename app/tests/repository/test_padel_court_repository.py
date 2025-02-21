import uuid
from decimal import Decimal

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.business import BusinessCreate
from app.models.padel_court import PadelCourtCreate
from app.repository.business_repository import BusinessRepository
from app.repository.padel_court_repository import PadelCourtRepository
from app.utilities.exceptions import (
    BusinessNotFoundException,
    UnauthorizedPadelCourtOperationException,
)


async def test_create_padel_court(session: AsyncSession):
    repository = BusinessRepository(session)
    business_data = BusinessCreate(name="Padel Ya", location="Av La plata 210")
    owner_id = uuid.uuid4()

    created_business = await repository.create_business(owner_id, business_data)

    repository = PadelCourtRepository(session)
    padel_court = PadelCourtCreate(name="Padel Si", price_per_hour=Decimal("15000.00"))

    created_padel_court = await repository.create_padel_court(
        owner_id, created_business.id, padel_court
    )

    assert created_padel_court.name == padel_court.name
    assert created_padel_court.price_per_hour == padel_court.price_per_hour


async def test_create_padel_court_with_nonexistent_business_id_return_exception(
    session: AsyncSession,
):
    repository = BusinessRepository(session)
    business_data = BusinessCreate(name="Padel Ya", location="Av La plata 3010")
    owner_id = uuid.uuid4()
    nonexistent_business_id = uuid.uuid4()

    created_business = await repository.create_business(owner_id, business_data)

    repository = PadelCourtRepository(session)
    padel_court = PadelCourtCreate(name="Padel Si", price_per_hour=Decimal("1500000"))

    with pytest.raises(BusinessNotFoundException) as e:
        await repository.create_padel_court(
            created_business.owner_id, nonexistent_business_id, padel_court
        )

    assert str(e.value) == "Business not found"


async def test_create_padel_court_with_unauthorized_owner_id_returns_exception(
    session: AsyncSession,
):
    repository = BusinessRepository(session)
    business_data = BusinessCreate(name="Padel Ya", location="Av La plata 210")
    owner_id = uuid.uuid4()

    created_business = await repository.create_business(owner_id, business_data)

    unauthorized_owner_id = uuid.uuid4()

    repository = PadelCourtRepository(session)
    padel_court = PadelCourtCreate(name="Cancha 5", price_per_hour=Decimal("12000"))

    with pytest.raises(UnauthorizedPadelCourtOperationException):
        await repository.create_padel_court(
            unauthorized_owner_id, created_business.id, padel_court
        )


async def test_get_padel_court(session: AsyncSession):
    repository = BusinessRepository(session)
    business_data = BusinessCreate(name="Padel Ya", location="Av La plata 210")
    owner_id = uuid.uuid4()

    created_business = await repository.create_business(owner_id, business_data)

    repository = PadelCourtRepository(session)
    padel_court = PadelCourtCreate(name="Padel Si", price_per_hour=Decimal("15000.00"))

    created_padel_court = await repository.create_padel_court(
        owner_id, created_business.id, padel_court
    )
    # test
    padel_court = await repository.get_padel_court("Padel Si", created_business.id)
    # assert

    assert padel_court.name == created_padel_court.name
    assert padel_court.price_per_hour == created_padel_court.price_per_hour