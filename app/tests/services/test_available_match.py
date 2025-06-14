import uuid
from datetime import date
from decimal import Decimal

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.available_match import AvailableMatchCreate
from app.models.business import BusinessCreate
from app.models.padel_court import PadelCourt, PadelCourtCreate
from app.repository.business_repository import BusinessRepository
from app.services.available_match_service import AvailableMatchService
from app.utilities.exceptions import (
    CourtAlreadyReservedException,
    NotFoundException,
    NotUniqueException,
    UnauthorizedUserException,
)


async def create_available_dates(session: AsyncSession) -> None:
    business_data = {"name": "Padel Ya", "location": "Av La plata 210"}
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()
    padel_court_data = {"name": "Padel Si", "price_per_hour": Decimal("15000.00")}
    padel_court_in = PadelCourtCreate(**padel_court_data)

    business_repository = BusinessRepository(session)
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

    service = AvailableMatchService()
    data_available_date = {
        "court_name": "35",
        "business_public_id": uuid.uuid4(),
        "date": date(2025, 1, 1),
        "court_public_id": new_padel_court.court_public_id,
        "initial_hour": 5,
        "n_matches": 5,
    }
    available_date_create = AvailableMatchCreate(**data_available_date)
    # test
    available_dates = await service.create_available_matches_in_date(
        session,
        owner_id,
        str(padel_court_data["name"]),
        business_public_id,
        available_date_create,
    )
    # assert
    assert len(available_dates) == 5


async def create_available_dates_invalid_not_unique(session: AsyncSession) -> None:
    business_data = {"name": "Padel Ya", "location": "Av La plata 210"}
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()
    padel_court_data = {"name": "Padel Si", "price_per_hour": Decimal("15000.00")}
    padel_court_in = PadelCourtCreate(**padel_court_data)

    business_repository = BusinessRepository(session)
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

    service = AvailableMatchService()
    data_available_date = {
        "court_name": "35",
        "business_public_id": uuid.uuid4(),
        "date": date(2025, 1, 1),
        "court_public_id": new_padel_court.court_public_id,
        "initial_hour": 5,
        "n_matches": 5,
    }
    available_date_create = AvailableMatchCreate(**data_available_date)
    await service.create_available_matches_in_date(
        session,
        owner_id,
        str(padel_court_data["name"]),
        business_public_id,
        available_date_create,
    )
    data_available_date_new = {
        "court_name": "35",
        "business_public_id": uuid.uuid4(),
        "date": date(2025, 1, 1),
        "court_public_id": new_padel_court.court_public_id,
        "initial_hour": 7,
        "n_matches": 1,
    }
    available_date_create_new = AvailableMatchCreate(**data_available_date_new)
    # test
    with pytest.raises(NotUniqueException) as e:
        await service.create_available_matches_in_date(
            session,
            owner_id,
            str(padel_court_data["name"]),
            business_public_id,
            available_date_create_new,
        )
    # assert
    assert e.value.detail == "Disponibilidad ya existente."


async def test_delete_empty_date(session: AsyncSession) -> None:
    business_data = {"name": "Padel Ya", "location": "Av La plata 210"}
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()
    padel_court_data = {"name": "Padel Si", "price_per_hour": Decimal("15000.00")}
    padel_court_in = PadelCourtCreate(**padel_court_data)

    business_repository = BusinessRepository(session)
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

    service = AvailableMatchService()
    # test
    await service.delete_available_matches_in_date(
        session,
        owner_id,
        str(padel_court_data["name"]),
        business_public_id,
        date(2025, 1, 1),
    )


async def test_delete_wrong_owner_id(session: AsyncSession) -> None:
    business_data = {"name": "Padel Ya", "location": "Av La plata 210"}
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()
    padel_court_data = {"name": "Padel Si", "price_per_hour": Decimal("15000.00")}
    padel_court_in = PadelCourtCreate(**padel_court_data)

    business_repository = BusinessRepository(session)
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

    not_owner = uuid.uuid4()
    limit = 100
    while not_owner == owner_id:
        not_owner = uuid.uuid4()
        limit -= 1
        assert limit != 0

    service = AvailableMatchService()
    # test
    with pytest.raises(UnauthorizedUserException) as e:
        await service.delete_available_matches_in_date(
            session,
            not_owner,
            str(padel_court_data["name"]),
            business_public_id,
            date(2025, 1, 1),
        )
    # assert
    assert e.value.detail == "No autorizado. Usuario no es el dueño"


async def test_delete(session: AsyncSession) -> None:
    business_data = {"name": "Padel Ya", "location": "Av La plata 210"}
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()
    padel_court_data = {"name": "Padel Si", "price_per_hour": Decimal("15000.00")}
    padel_court_in = PadelCourtCreate(**padel_court_data)

    business_repository = BusinessRepository(session)
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

    create_date = date(2025, 1, 1)

    service = AvailableMatchService()
    data_available_date = {
        "court_name": "35",
        "business_public_id": uuid.uuid4(),
        "court_public_id": new_padel_court.court_public_id,
        "date": create_date,
        "initial_hour": 5,
        "n_matches": 5,
    }
    available_date_create = AvailableMatchCreate(**data_available_date)
    await service.create_available_matches_in_date(
        session,
        owner_id,
        str(padel_court_data["name"]),
        business_public_id,
        available_date_create,
    )
    # test
    await service.delete_available_matches_in_date(
        session,
        owner_id,
        str(padel_court_data["name"]),
        business_public_id,
        create_date,
    )
    response_get = await service.get_available_matches_in_date(
        session, str(padel_court_data["name"]), business_public_id, create_date
    )
    # assert
    assert len(response_get) == 0


async def test_reserve_match(session: AsyncSession) -> None:
    business_data = {"name": "Padel Ya", "location": "Av La plata 210"}
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()
    padel_court_data = {"name": "Padel Si", "price_per_hour": Decimal("15000.00")}
    padel_court_in = PadelCourtCreate(**padel_court_data)

    business_repository = BusinessRepository(session)
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

    create_date = date(2025, 1, 1)

    service = AvailableMatchService()
    data_available_date = {
        "court_name": str(padel_court_data["name"]),
        "business_public_id": business_public_id,
        "date": create_date,
        "court_public_id": new_padel_court.court_public_id,
        "initial_hour": 5,
        "n_matches": 1,
    }
    available_date_create = AvailableMatchCreate(**data_available_date)
    list = await service.create_available_matches_in_date(
        session,
        owner_id,
        str(padel_court_data["name"]),
        business_public_id,
        available_date_create,
    )
    assert len(list) == 1
    # test
    match = await service.reserve_available_match(
        session, str(padel_court_data["name"]), business_public_id, create_date, 5
    )
    # assert
    assert match is not None
    assert match.is_reserved()


async def test_reserve_match_not_found(session: AsyncSession) -> None:
    # test
    business_public_id = uuid.uuid4()
    create_date = date(2025, 1, 1)
    service = AvailableMatchService()
    with pytest.raises(NotFoundException) as e:
        await service.reserve_available_match(
            session, "name", business_public_id, create_date, 5
        )
    assert e.value.detail == "No se encontró Disponibilidad para el match"


async def test_reserve_match_already_reserved_raise_CourtAlreadyReservedException(
    session: AsyncSession,
) -> None:
    business_data = {"name": "Padel Ya", "location": "Av La plata 210"}
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()
    padel_court_data = {"name": "Padel Si", "price_per_hour": Decimal("15000.00")}
    padel_court_in = PadelCourtCreate(**padel_court_data)

    business_repository = BusinessRepository(session)
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

    create_date = date(2025, 1, 1)

    service = AvailableMatchService()
    data_available_date = {
        "court_name": str(padel_court_data["name"]),
        "business_public_id": business_public_id,
        "date": create_date,
        "court_public_id": new_padel_court.court_public_id,
        "initial_hour": 5,
        "n_matches": 1,
    }
    available_date_create = AvailableMatchCreate(**data_available_date)
    list = await service.create_available_matches_in_date(
        session,
        owner_id,
        str(padel_court_data["name"]),
        business_public_id,
        available_date_create,
    )
    assert len(list) == 1
    match = await service.reserve_available_match(
        session, str(padel_court_data["name"]), business_public_id, create_date, 5
    )
    assert match is not None
    assert match.is_reserved()
    # test
    with pytest.raises(CourtAlreadyReservedException) as e:
        await service.reserve_available_match(
            session, str(padel_court_data["name"]), business_public_id, create_date, 5
        )
    # assert
    assert (
        e.value.detail == f"La cancha {str(padel_court_data['name'])} está reservada."
    )
