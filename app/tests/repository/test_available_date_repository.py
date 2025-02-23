import uuid
import datetime

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from decimal import Decimal
from app.models.available_date import AvailableDateCreate
from app.models.business import BusinessCreate
from app.models.padel_court import PadelCourtCreate, PadelCourt
from app.repository.available_date_repository import AvailableDateRepository
from app.repository.business_repository import BusinessRepository
from app.utilities.exceptions import NotFoundException, CourtAlreadyReservedException


async def test_create_available_dates(session: AsyncSession) -> None:
    business_repository = BusinessRepository(session)
    business_data = {
        "name":"Padel Ya",
        "location": "Av La plata 210"
    }
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()
    padel_court_data = {
        "name":"Padel Si",
        "price_per_hour":Decimal("15000.00")
    }
    padel_court_in = PadelCourtCreate(**padel_court_data)
    created_business = await business_repository.create_business(owner_id, business)
    business_id = created_business.id
    new_padel_court = PadelCourt.model_validate(
        padel_court_in, update={"business_id": business_id}
    )
    session.add(new_padel_court)
    await session.commit()
    await session.refresh(new_padel_court)

    available_date_create_data = {
        "court_name": padel_court_data["name"],
        "business_id": business_id,
        "date": datetime.date(2025, 1, 1),
        "initial_hour": 5,
        "number_of_games": 5
    }

    repository_available_date = AvailableDateRepository(session)
    create = AvailableDateCreate(**available_date_create_data)
    # test
    dates = await repository_available_date.create_available_dates(create)
    # assert
    assert len(dates) == 5


async def test_get_available_dates(session: AsyncSession) -> None:
    business_repository = BusinessRepository(session)
    business_data = {
        "name":"Padel Ya",
        "location": "Av La plata 210"
    }
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()
    padel_court_data = {
        "name":"Padel Si",
        "price_per_hour":Decimal("15000.00")
    }
    padel_court_in = PadelCourtCreate(**padel_court_data)
    created_business = await business_repository.create_business(owner_id, business)
    business_id = created_business.id
    new_padel_court = PadelCourt.model_validate(
        padel_court_in, update={"business_id": business_id}
    )
    session.add(new_padel_court)
    await session.commit()
    await session.refresh(new_padel_court)

    available_date_create_date = datetime.date(2025, 1, 1)

    available_date_create_data = {
        "court_name": padel_court_data["name"],
        "business_id": business_id,
        "date": available_date_create_date,
        "initial_hour": 5,
        "number_of_games": 5
    }

    repository_available_date = AvailableDateRepository(session)
    create = AvailableDateCreate(**available_date_create_data)
    await repository_available_date.create_available_dates(create)
    # test
    dates = await repository_available_date.get_available_dates(padel_court_data["name"], business_id, available_date_create_date)
    # assert
    assert len(dates) == 5


async def test_get_not_available_dates(session: AsyncSession) -> None:
    business_repository = BusinessRepository(session)
    business_data = {
        "name":"Padel Ya",
        "location": "Av La plata 210"
    }
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()
    padel_court_data = {
        "name":"Padel Si",
        "price_per_hour":Decimal("15000.00")
    }
    padel_court_in = PadelCourtCreate(**padel_court_data)
    created_business = await business_repository.create_business(owner_id, business)
    business_id = created_business.id
    new_padel_court = PadelCourt.model_validate(
        padel_court_in, update={"business_id": business_id}
    )
    session.add(new_padel_court)
    await session.commit()
    await session.refresh(new_padel_court)

    available_date_create_date = datetime.date(2025, 1, 1)

    available_date_create_data = {
        "court_name": padel_court_data["name"],
        "business_id": business_id,
        "date": available_date_create_date,
        "initial_hour": 5,
        "number_of_games": 5
    }

    repository_available_date = AvailableDateRepository(session)
    create = AvailableDateCreate(**available_date_create_data)
    await repository_available_date.create_available_dates(create)

    date_whitout_available_dates = datetime.date(2025, 1, 2)
    # test
    dates = await repository_available_date.get_available_dates(padel_court_data["name"], business_id, date_whitout_available_dates)
    # assert
    assert len(dates) == 0


async def test_get_not_created_available_dates(session: AsyncSession) -> None:
    repository_available_date = AvailableDateRepository(session)
    date_whitout_available_dates = datetime.date(2025, 1, 2)
    business_id = uuid.uuid4()
    padel_court_name = "Padel Si"
    # test
    dates = await repository_available_date.get_available_dates(padel_court_name, business_id, date_whitout_available_dates)
    # assert
    assert len(dates) == 0


async def test_delete_available_dates(session: AsyncSession) -> None:
    business_repository = BusinessRepository(session)
    business_data = {
        "name":"Padel Ya",
        "location": "Av La plata 210"
    }
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()
    padel_court_data = {
        "name":"Padel Si",
        "price_per_hour":Decimal("15000.00")
    }
    padel_court_in = PadelCourtCreate(**padel_court_data)
    created_business = await business_repository.create_business(owner_id, business)
    business_id = created_business.id
    new_padel_court = PadelCourt.model_validate(
        padel_court_in, update={"business_id": business_id}
    )
    session.add(new_padel_court)
    await session.commit()
    await session.refresh(new_padel_court)

    available_date_create_date = datetime.date(2025, 1, 1)
    available_date_create_data = {
        "court_name": padel_court_data["name"],
        "business_id": business_id,
        "date": available_date_create_date,
        "initial_hour": 5,
        "number_of_games": 5
    }

    repository_available_date = AvailableDateRepository(session)
    create = AvailableDateCreate(**available_date_create_data)
    await repository_available_date.create_available_dates(create)
    # test
    await repository_available_date.delete_available_date(padel_court_data["name"], business_id, available_date_create_date)
    dates = await repository_available_date.get_available_dates(padel_court_data["name"], business_id, available_date_create_date)
    # assert
    assert len(dates) == 0


async def test_delete_not_created_available_dates(session: AsyncSession) -> None:
    repository_available_date = AvailableDateRepository(session)
    date_whitout_available_dates = datetime.date(2025, 1, 2)
    business_id = uuid.uuid4()
    padel_court_name = "Padel Si"
    # test
    await repository_available_date.delete_available_date(padel_court_name, business_id, date_whitout_available_dates)
    dates = await repository_available_date.get_available_dates(padel_court_name, business_id, date_whitout_available_dates)
    # assert
    assert len(dates) == 0


async def test_update_to_reserve_invalid_available_dates_not_exist(session: AsyncSession) -> None:
    repository_available_date = AvailableDateRepository(session)
    date_whitout_available_dates = datetime.date(2025, 1, 2)
    business_id = uuid.uuid4()
    padel_court_name = "Padel Si"
    # test

    with pytest.raises(NotFoundException) as e:
        await repository_available_date.update_to_reserve_available_date(padel_court_name, business_id, date_whitout_available_dates, 8)
    # assert
    assert e.value.detail == "Available date not found"


async def test_update_to_reserve_available_date(session: AsyncSession) -> None:
    business_repository = BusinessRepository(session)
    business_data = {
        "name":"Padel Ya",
        "location": "Av La plata 210"
    }
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()
    padel_court_data = {
        "name":"Padel Si",
        "price_per_hour":Decimal("15000.00")
    }
    padel_court_in = PadelCourtCreate(**padel_court_data)
    created_business = await business_repository.create_business(owner_id, business)
    business_id = created_business.id
    new_padel_court = PadelCourt.model_validate(
        padel_court_in, update={"business_id": business_id}
    )
    session.add(new_padel_court)
    await session.commit()
    await session.refresh(new_padel_court)

    available_date_create_date = datetime.date(2025, 1, 1)
    available_date_create_data = {
        "court_name": padel_court_data["name"],
        "business_id": business_id,
        "date": available_date_create_date,
        "initial_hour": 5,
        "number_of_games": 1
    }

    repository_available_date = AvailableDateRepository(session)
    create = AvailableDateCreate(**available_date_create_data)
    await repository_available_date.create_available_dates(create)
    # test
    date = await repository_available_date.update_to_reserve_available_date(padel_court_data["name"], business_id, available_date_create_date, 5)
    dates = await repository_available_date.get_available_dates(padel_court_data["name"], business_id, available_date_create_date)
    # assert
    assert len(dates) == 1
    assert dates[0].get_is_reserved()
    assert date.get_is_reserved()


async def test_update_to_reserve_court_reserved_available_date_invalid(session: AsyncSession) -> None:
    business_repository = BusinessRepository(session)
    business_data = {
        "name":"Padel Ya",
        "location": "Av La plata 210"
    }
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()
    padel_court_data = {
        "name":"Padel Si",
        "price_per_hour":Decimal("15000.00")
    }
    padel_court_in = PadelCourtCreate(**padel_court_data)
    created_business = await business_repository.create_business(owner_id, business)
    business_id = created_business.id
    new_padel_court = PadelCourt.model_validate(
        padel_court_in, update={"business_id": business_id}
    )
    session.add(new_padel_court)
    await session.commit()
    await session.refresh(new_padel_court)

    available_date_create_date = datetime.date(2025, 1, 1)
    available_date_create_data = {
        "court_name": padel_court_data["name"],
        "business_id": business_id,
        "date": available_date_create_date,
        "initial_hour": 5,
        "number_of_games": 1
    }

    repository_available_date = AvailableDateRepository(session)
    create = AvailableDateCreate(**available_date_create_data)
    await repository_available_date.create_available_dates(create)
    # test
    await repository_available_date.update_to_reserve_available_date(padel_court_data["name"], business_id, available_date_create_date, 5)
    with pytest.raises(CourtAlreadyReservedException) as e:
        await repository_available_date.update_to_reserve_available_date(padel_court_data["name"], business_id, available_date_create_date, 5)
    # assert
    assert e.value.detail == f"The court {padel_court_data["name"]} is already reserved."