import uuid
from datetime import date

import pytest

from app.models.available_match import (
    AvailableMatch,
    AvailableMatchCreate,
    AvailableMatchesPublic,
    AvailableMatchPublic,
)
from app.utilities.exceptions import NotAcceptableException


async def test_one_available_date_form_create() -> None:
    data = {
        "court_name": "25",
        "business_public_id": uuid.uuid4(),
        "date": date(2025, 1, 1),
        "court_public_id": uuid.uuid4(),
        "initial_hour": 23,
        "n_matches": 1,
    }
    create = AvailableMatchCreate(**data)
    create.validate_create()
    # test
    available_date_list: list[AvailableMatch] = AvailableMatch.from_create(create)
    # assert
    assert len(available_date_list) == 1
    available_date = available_date_list[0]
    for key, value in data.items():
        if key == "n_matches":
            continue
        assert getattr(available_date, key) == value
    assert available_date.reserve is False


async def test_more_available_date_form_create() -> None:
    data = {
        "court_name": "35",
        "business_public_id": uuid.uuid4(),
        "date": date(2025, 1, 1),
        "court_public_id": uuid.uuid4(),
        "initial_hour": 5,
        "n_matches": 5,
    }
    initial_hour_list = [5, 6, 7, 8, 9]
    create = AvailableMatchCreate(**data)
    create.validate_create()
    # test
    available_date_list: list[AvailableMatch] = AvailableMatch.from_create(create)
    # assert
    assert len(available_date_list) == 5
    for available_date in available_date_list:
        for key, value in data.items():
            if key == "n_matches":
                continue
            elif key == "initial_hour":
                initial_hour = getattr(available_date, key)
                assert initial_hour in initial_hour_list
                initial_hour_list.remove(initial_hour)
                continue
            assert getattr(available_date, key) == value
        assert available_date.reserve is False


async def test_limit_available_date_form_create() -> None:
    data = {
        "court_name": "4",
        "business_public_id": uuid.uuid4(),
        "date": date(2025, 1, 1),
        "court_public_id": uuid.uuid4(),
        "initial_hour": 0,
        "n_matches": 24,
    }
    initial_hour_list = [False] * 24
    create = AvailableMatchCreate(**data)
    create.validate_create()
    # test
    available_date_list: list[AvailableMatch] = AvailableMatch.from_create(create)
    # assert
    assert len(available_date_list) == 24
    for available_date in available_date_list:
        for key, value in data.items():
            if key == "n_matches":
                continue
            elif key == "initial_hour":
                pos = getattr(available_date, key)
                initial_hour_list[pos] = True
                continue
            assert getattr(available_date, key) == value
        assert available_date.reserve is False
    for initial_hour in initial_hour_list:
        assert initial_hour


async def test_create_invalid_exceed_hour() -> None:
    data = {
        "court_name": "7",
        "business_public_id": uuid.uuid4(),
        "date": date(2025, 1, 1),
        "court_public_id": uuid.uuid4(),
        "initial_hour": 23,
        "n_matches": 2,
    }
    # test
    create = AvailableMatchCreate(**data)
    # assert
    with pytest.raises(NotAcceptableException) as e:
        create.validate_create()
    assert (
        e.value.detail
        == "The information is not acceptable. Reason: n_matches cannot exceed the time of one day."
    )


async def test_create_invalid_number_games() -> None:
    data = {
        "court_name": "8",
        "business_public_id": uuid.uuid4(),
        "date": date(2025, 1, 1),
        "court_public_id": uuid.uuid4(),
        "initial_hour": 12,
        "n_matches": 0,
    }
    # test
    create = AvailableMatchCreate(**data)
    # assert
    with pytest.raises(NotAcceptableException) as e:
        create.validate_create()
    assert (
        e.value.detail
        == "The information is not acceptable. Reason: n_matches cannot be less than 0."
    )


async def test_available_date_set_reserve() -> None:
    data = {
        "id": 15,
        "court_name": "8",
        "business_public_id": uuid.uuid4(),
        "date": date(2025, 1, 1),
        "court_public_id": uuid.uuid4(),
        "initial_hour": 23,
        "is_reserved": False,
    }
    available_date = AvailableMatch(**data)
    # test
    available_date.set_reserve()
    # assert
    assert available_date.reserve is True


async def test_public_from_private() -> None:
    data = {
        "id": 15,
        "court_name": "35",
        "business_public_id": uuid.uuid4(),
        "date": date(2025, 1, 1),
        "court_public_id": uuid.uuid4(),
        "initial_hour": 23,
        "reserve": False,
    }
    available_date = AvailableMatch(**data)
    coordinates = (0.1, 0.5)
    data["latitude"] = coordinates[0]
    data["longitude"] = coordinates[1]
    # test
    available_date_public = AvailableMatchPublic.from_private(
        available_date, coordinates
    )
    # assert
    for key, value in data.items():
        if key == "id":
            continue
        assert getattr(available_date_public, key) == value


async def test_publics_from_private() -> None:
    data = {
        "id": 15,
        "court_name": "7",
        "business_public_id": uuid.uuid4(),
        "date": date(2025, 1, 1),
        "court_public_id": uuid.uuid4(),
        "initial_hour": 23,
        "reserve": False,
    }
    available_date = AvailableMatch(**data)
    coordinates = (0.1, 0.5)
    data["latitude"] = coordinates[0]
    data["longitude"] = coordinates[1]
    # test
    available_dates_public = AvailableMatchesPublic.from_private(
        [available_date], coordinates
    )
    # assert
    assert available_dates_public.count == 1
    available_date_public = available_dates_public.data[0]
    for key, value in data.items():
        if key == "id":
            continue
        assert getattr(available_date_public, key) == value
