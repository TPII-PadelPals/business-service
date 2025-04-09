import datetime
import uuid
from decimal import Decimal

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.available_match import AvailableMatchCreate
from app.models.business import BusinessCreate
from app.models.padel_court import PadelCourt, PadelCourtCreate
from app.repository.available_matches_repository import AvailableMatchesRepository
from app.repository.business_repository import BusinessRepository
from app.utilities.exceptions import NotFoundException


async def test_create_available_dates(session: AsyncSession) -> None:
    business_repository = BusinessRepository(session)
    business_data = {"name": "Padel Ya", "location": "Av La plata 210"}
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()
    padel_court_data = {"name": "Padel Si", "price_per_hour": Decimal("15000.00")}
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

    available_date_create_data = {
        "court_name": padel_court_data["name"],
        "business_public_id": business_public_id,
        "date": datetime.date(2025, 1, 1),
        "court_public_id": new_padel_court.court_public_id,
        "initial_hour": 5,
        "n_matches": 5,
    }

    repository_available_date = AvailableMatchesRepository(session)
    create = AvailableMatchCreate(**available_date_create_data)
    # test
    dates = await repository_available_date.create_available_matches_in_date(create)
    # assert
    assert len(dates) == 5


async def test_get_available_dates(session: AsyncSession) -> None:
    business_repository = BusinessRepository(session)
    business_data = {"name": "Padel Ya", "location": "Av La plata 210"}
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()
    padel_court_data = {"name": "Padel Si", "price_per_hour": Decimal("15000.00")}
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

    available_date_create_date = datetime.date(2025, 1, 1)

    available_date_create_data = {
        "court_name": padel_court_data["name"],
        "business_public_id": business_public_id,
        "date": available_date_create_date,
        "court_public_id": new_padel_court.court_public_id,
        "initial_hour": 5,
        "n_matches": 5,
    }

    repository_available_date = AvailableMatchesRepository(session)
    create = AvailableMatchCreate(**available_date_create_data)
    await repository_available_date.create_available_matches_in_date(create)
    # test
    dates = await repository_available_date.get_available_matches_in_date(
        str(padel_court_data["name"]), business_public_id, available_date_create_date
    )
    # assert
    assert len(dates) == 5


async def test_get_not_available_dates(session: AsyncSession) -> None:
    business_repository = BusinessRepository(session)
    business_data = {"name": "Padel Ya", "location": "Av La plata 210"}
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()
    padel_court_data = {"name": "Padel Si", "price_per_hour": Decimal("15000.00")}
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

    available_date_create_date = datetime.date(2025, 1, 1)

    available_date_create_data = {
        "court_name": padel_court_data["name"],
        "business_public_id": business_public_id,
        "date": available_date_create_date,
        "court_public_id": new_padel_court.court_public_id,
        "initial_hour": 5,
        "n_matches": 5,
    }

    repository_available_date = AvailableMatchesRepository(session)
    create = AvailableMatchCreate(**available_date_create_data)
    await repository_available_date.create_available_matches_in_date(create)

    date_whitout_available_dates = datetime.date(2025, 1, 2)
    # test
    dates = await repository_available_date.get_available_matches_in_date(
        str(padel_court_data["name"]), business_public_id, date_whitout_available_dates
    )
    # assert
    assert len(dates) == 0


async def test_get_not_created_available_dates(session: AsyncSession) -> None:
    repository_available_date = AvailableMatchesRepository(session)
    date_whitout_available_dates = datetime.date(2025, 1, 2)
    business_public_id = uuid.uuid4()
    padel_court_name = "Padel Si"
    # test
    dates = await repository_available_date.get_available_matches_in_date(
        padel_court_name, business_public_id, date_whitout_available_dates
    )
    # assert
    assert len(dates) == 0


async def test_delete_available_dates(session: AsyncSession) -> None:
    business_repository = BusinessRepository(session)
    business_data = {"name": "Padel Ya", "location": "Av La plata 210"}
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()
    padel_court_data = {"name": "Padel Si", "price_per_hour": Decimal("15000.00")}
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

    available_date_create_date = datetime.date(2025, 1, 1)
    available_date_create_data = {
        "court_name": padel_court_data["name"],
        "business_public_id": business_public_id,
        "date": available_date_create_date,
        "court_public_id": new_padel_court.court_public_id,
        "initial_hour": 5,
        "n_matches": 5,
    }

    repository_available_date = AvailableMatchesRepository(session)
    create = AvailableMatchCreate(**available_date_create_data)
    await repository_available_date.create_available_matches_in_date(create)
    # test
    await repository_available_date.delete_available_matches_in_date(
        str(padel_court_data["name"]), business_public_id, available_date_create_date
    )
    dates = await repository_available_date.get_available_matches_in_date(
        str(padel_court_data["name"]), business_public_id, available_date_create_date
    )
    # assert
    assert len(dates) == 0


async def test_delete_not_created_available_dates(session: AsyncSession) -> None:
    repository_available_date = AvailableMatchesRepository(session)
    date_whitout_available_dates = datetime.date(2025, 1, 2)
    business_public_id = uuid.uuid4()
    padel_court_name = "Padel Si"
    # test
    await repository_available_date.delete_available_matches_in_date(
        padel_court_name, business_public_id, date_whitout_available_dates
    )
    dates = await repository_available_date.get_available_matches_in_date(
        padel_court_name, business_public_id, date_whitout_available_dates
    )
    # assert
    assert len(dates) == 0


async def test_get_specific_match_invalid_available_match_not_exist(
    session: AsyncSession,
) -> None:
    repository_available_date = AvailableMatchesRepository(session)
    date_whitout_available_dates = datetime.date(2025, 1, 2)
    business_public_id = uuid.uuid4()
    padel_court_name = "Padel Si"
    # test

    with pytest.raises(NotFoundException) as e:
        await repository_available_date.get_available_match(
            padel_court_name, business_public_id, date_whitout_available_dates, 8
        )
    # assert
    assert e.value.detail == "Available match not found"


async def test_update_to_reserve_available_date(session: AsyncSession) -> None:
    business_repository = BusinessRepository(session)
    business_data = {"name": "Padel Ya", "location": "Av La plata 210"}
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()
    padel_court_data = {"name": "Padel Si", "price_per_hour": Decimal("15000.00")}
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

    available_date_create_date = datetime.date(2025, 1, 1)
    available_date_create_data = {
        "court_name": padel_court_data["name"],
        "business_public_id": business_public_id,
        "date": available_date_create_date,
        "court_public_id": new_padel_court.court_public_id,
        "initial_hour": 5,
        "n_matches": 1,
    }

    repository_available_date = AvailableMatchesRepository(session)
    create = AvailableMatchCreate(**available_date_create_data)
    await repository_available_date.create_available_matches_in_date(create)
    date = await repository_available_date.get_available_match(
        str(padel_court_data["name"]), business_public_id, available_date_create_date, 5
    )
    assert not date.is_reserved()
    date.set_reserve()
    # test
    date = await repository_available_date.update_available_match(date)
    dates = await repository_available_date.get_available_matches_in_date(
        str(padel_court_data["name"]), business_public_id, available_date_create_date
    )
    # assert
    assert len(dates) == 1
    assert dates[0].is_reserved()
    assert date.is_reserved()
