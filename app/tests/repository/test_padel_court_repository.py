import uuid
from decimal import Decimal

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.business import BusinessCreate
from app.models.padel_court import PadelCourt, PadelCourtCreate
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

    longitude = 0.1
    latitude = 0.4
    created_business = await repository.create_business(
        owner_id, business_data, longitude, latitude
    )

    repository = PadelCourtRepository(session)
    padel_court = PadelCourtCreate(name="Padel Si", price_per_hour=Decimal("15000.00"))

    created_padel_court = await repository.create_padel_court(
        owner_id, created_business.business_public_id, padel_court
    )

    assert created_padel_court.name == padel_court.name
    assert created_padel_court.price_per_hour == padel_court.price_per_hour


async def test_create_padel_court_with_nonexistent_business_public_id_return_exception(
    session: AsyncSession,
):
    repository = BusinessRepository(session)
    business_data = BusinessCreate(name="Padel Ya", location="Av La plata 3010")
    owner_id = uuid.uuid4()
    nonexistent_business_public_id = uuid.uuid4()

    longitude = 0.1
    latitude = 0.4
    created_business = await repository.create_business(
        owner_id, business_data, longitude, latitude
    )

    repository = PadelCourtRepository(session)
    padel_court = PadelCourtCreate(name="Padel Si", price_per_hour=Decimal("1500000"))

    with pytest.raises(BusinessNotFoundException) as e:
        await repository.create_padel_court(
            created_business.owner_id, nonexistent_business_public_id, padel_court
        )

    assert str(e.value) == "No se encontró establecimiento"


async def test_create_padel_court_with_unauthorized_owner_id_returns_exception(
    session: AsyncSession,
):
    business_repository = BusinessRepository(session)
    business_data = BusinessCreate(name="Padel Ya", location="Av La plata 210")
    owner_id = uuid.uuid4()

    longitude = 0.1
    latitude = 0.4
    created_business = await business_repository.create_business(
        owner_id, business_data, longitude, latitude
    )

    unauthorized_owner_id = uuid.uuid4()

    padel_court_repository = PadelCourtRepository(session)
    padel_court = PadelCourtCreate(name="Cancha 5", price_per_hour=Decimal("12000"))

    with pytest.raises(UnauthorizedPadelCourtOperationException):
        await padel_court_repository.create_padel_court(
            unauthorized_owner_id, created_business.business_public_id, padel_court
        )


async def test_get_padel_court(session: AsyncSession) -> None:
    business_repository = BusinessRepository(session)
    business_data = {"name": "Padel Ya", "location": "Av La plata 210"}
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()
    padel_court_data = {"name": "Padel Si", "price_per_hour": Decimal("15000.00")}
    padel_court_repository = PadelCourtRepository(session)
    padel_court_in = PadelCourtCreate(**padel_court_data)
    longitude = 0.1
    latitude = 0.4
    created_business = await business_repository.create_business(
        owner_id, business, longitude, latitude
    )
    business_public_id = created_business.business_public_id
    new_padel_court = PadelCourt.model_validate(
        padel_court_in, update={"business_public_id": business_public_id}
    )
    session.add(new_padel_court)
    await session.commit()
    await session.refresh(new_padel_court)
    # test
    padel_court = await padel_court_repository.get_padel_court(
        str(padel_court_data["name"]), business_public_id
    )
    # assert

    assert padel_court.name == padel_court_data["name"]
    assert padel_court.price_per_hour == padel_court_data["price_per_hour"]


async def test_get_all_padel_courts(session: AsyncSession) -> None:
    business_repo = BusinessRepository(session)
    padel_court_repo = PadelCourtRepository(session)
    owner_id = uuid.uuid4()
    coords = (0.1, 0.4)

    business1 = await business_repo.create_business(
        owner_id,
        BusinessCreate(name="Business Alpha", location="Location Alpha"),
        *coords,
    )
    business2 = await business_repo.create_business(
        owner_id,
        BusinessCreate(name="Business Beta", location="Location Beta"),
        *coords,
    )

    court1 = PadelCourtCreate(name="Court A", price_per_hour=Decimal("100.00"))
    court2 = PadelCourtCreate(name="Court B", price_per_hour=Decimal("150.00"))
    court3 = PadelCourtCreate(name="Court C", price_per_hour=Decimal("200.00"))

    await padel_court_repo.create_padel_court(
        owner_id, business1.business_public_id, court1
    )
    await padel_court_repo.create_padel_court(
        owner_id, business1.business_public_id, court2
    )
    await padel_court_repo.create_padel_court(
        owner_id, business2.business_public_id, court3
    )

    result = await padel_court_repo.get_padel_courts()

    assert result.count >= 3
    assert len(result.data) >= 3
    court_names = [c.name for c in result.data]
    assert "Court A" in court_names
    assert "Court B" in court_names
    assert "Court C" in court_names


async def test_get_padel_courts_filtered_by_business(session: AsyncSession) -> None:
    business_repo = BusinessRepository(session)
    padel_court_repo = PadelCourtRepository(session)
    owner_id = uuid.uuid4()
    coords = (0.1, 0.4)

    business1 = await business_repo.create_business(
        owner_id,
        BusinessCreate(name="Filter Business A", location="Location A"),
        *coords,
    )
    business2 = await business_repo.create_business(
        owner_id,
        BusinessCreate(name="Filter Business B", location="Location B"),
        *coords,
    )

    court1 = PadelCourtCreate(name="Filter Court X", price_per_hour=Decimal("100.00"))
    court2 = PadelCourtCreate(name="Filter Court Y", price_per_hour=Decimal("150.00"))
    court3 = PadelCourtCreate(name="Filter Court Z", price_per_hour=Decimal("200.00"))

    await padel_court_repo.create_padel_court(
        owner_id, business1.business_public_id, court1
    )
    await padel_court_repo.create_padel_court(
        owner_id, business1.business_public_id, court2
    )
    await padel_court_repo.create_padel_court(
        owner_id, business2.business_public_id, court3
    )

    result = await padel_court_repo.get_padel_courts(
        business_public_id=business1.business_public_id, user_id=owner_id
    )

    assert result.count == 2
    assert len(result.data) == 2
    court_names = [c.name for c in result.data]
    assert "Filter Court X" in court_names
    assert "Filter Court Y" in court_names
    assert "Filter Court Z" not in court_names


async def test_get_padel_courts_with_pagination(session: AsyncSession) -> None:
    business_repo = BusinessRepository(session)
    padel_court_repo = PadelCourtRepository(session)
    owner_id = uuid.uuid4()
    coords = (0.1, 0.4)

    business = await business_repo.create_business(
        owner_id,
        BusinessCreate(name="Pagination Business", location="Location"),
        *coords,
    )

    for i in range(1, 6):
        court = PadelCourtCreate(
            name=f"Paginated Court {i}", price_per_hour=Decimal(f"{100.0 + i}")
        )
        await padel_court_repo.create_padel_court(
            owner_id, business.business_public_id, court
        )

    page1 = await padel_court_repo.get_padel_courts(
        business_public_id=business.business_public_id, skip=0, limit=2
    )

    page2 = await padel_court_repo.get_padel_courts(
        business_public_id=business.business_public_id, skip=2, limit=2
    )

    assert page1.count >= 5
    assert len(page1.data) == 2

    assert page2.count >= 5
    assert len(page2.data) == 2

    page1_names = [c.name for c in page1.data]
    page2_names = [c.name for c in page2.data]
    assert not any(name in page1_names for name in page2_names)
