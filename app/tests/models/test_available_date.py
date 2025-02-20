import uuid

from datetime import date

import pytest

from app.models.available_date import AvailableDateCreate, AvailableDate, AvailableDatePublic, AvailableDatesPublic
from app.utilities.exceptions import NotAcceptableException


async def test_one_available_date_form_create() -> None:
    data = {
        "court_id": uuid.uuid4(),
        "business_id": uuid.uuid4(),
        "date": date(2025, 1, 1),
        "initial_hour": 23,
        "number_of_games":1,
    }
    create = AvailableDateCreate(**data)
    create.validate_create()
    # test
    available_date_list: list[AvailableDate] = AvailableDate.from_create(create)
    # assert
    assert len(available_date_list) == 1
    available_date = available_date_list[0]
    for key, value in data.items():
        assert getattr(available_date, key) == value
    assert available_date.is_reserved is False


async def test_more_available_date_form_create() -> None:
    data = {
        "court_id": uuid.uuid4(),
        "business_id": uuid.uuid4(),
        "date": date(2025, 1, 1),
        "initial_hour": 5,
        "number_of_games":5,
    }
    initial_hour_list = [5, 6, 7, 8, 9]
    create = AvailableDateCreate(**data)
    create.validate_create()
    # test
    available_date_list: list[AvailableDate] = AvailableDate.from_create(create)
    # assert
    assert len(available_date_list) == 5
    for available_date in available_date_list:
        for key, value in data.items():
            if key == "initial_hour":
                data = getattr(available_date, key)
                assert data in initial_hour_list
                initial_hour_list.remove(data)
                continue
            assert getattr(available_date, key) == value
        assert available_date.is_reserved is False


async def test_limit_available_date_form_create() -> None:
    data = {
        "court_id": uuid.uuid4(),
        "business_id": uuid.uuid4(),
        "date": date(2025, 1, 1),
        "initial_hour": 0,
        "number_of_games":23,
    }
    initial_hour_list = [False] * 24
    create = AvailableDateCreate(**data)
    create.validate_create()
    # test
    available_date_list: list[AvailableDate] = AvailableDate.from_create(create)
    # assert
    assert len(available_date_list) == 24
    for available_date in available_date_list:
        for key, value in data.items():
            if key == "initial_hour":
                pos = getattr(available_date, key)
                initial_hour_list[pos] = True
                continue
            assert getattr(available_date, key) == value
        assert available_date.is_reserved is False
    for initial_hour in initial_hour_list:
        assert initial_hour


async def test_create_invalid_exceed_hour() -> None:
    data = {
        "court_id": uuid.uuid4(),
        "business_id": uuid.uuid4(),
        "date": date(2025, 1, 1),
        "initial_hour": 23,
        "number_of_games":2,
    }
    # test
    create = AvailableDateCreate(**data)
    # assert
    with pytest.raises(NotAcceptableException) as e:
        create.validate_create()
    assert e.value.detail == "The information is not acceptable. Reason: number_of_games cannot exceed the time of one day."


async def test_create_invalid_number_games() -> None:
    data = {
        "court_id": uuid.uuid4(),
        "business_id": uuid.uuid4(),
        "date": date(2025, 1, 1),
        "initial_hour": 12,
        "number_of_games":0,
    }
    # test
    create = AvailableDateCreate(**data)
    # assert
    with pytest.raises(NotAcceptableException) as e:
        create.validate_create()
    assert e.value.detail == "The information is not acceptable. Reason: number_of_games cannot be less than 0."


async def test_available_date_set_reserve() -> None:
    data = {
        "id": 15,
        "court_id": uuid.uuid4(),
        "business_id": uuid.uuid4(),
        "date": date(2025, 1, 1),
        "initial_hour": 23,
        "number_of_games":1,
        "is_reserved": False
    }
    available_date = AvailableDate(**data)
    # test
    available_date.set_reserve()
    # assert
    assert available_date.is_reserved is True


async def test_public_from_private() -> None:
    data = {
        "id": 15,
        "court_id": uuid.uuid4(),
        "business_id": uuid.uuid4(),
        "date": date(2025, 1, 1),
        "initial_hour": 23,
        "number_of_games":1,
        "is_reserved": False
    }
    available_date = AvailableDate(**data)
    # test
    available_date_public = AvailableDatePublic.from_private(available_date)
    # assert
    for key, value in data.items():
        if key == "id":
            continue
        assert getattr(available_date_public, key) == value


async def test_publics_from_private() -> None:
    data = {
        "id": 15,
        "court_id": uuid.uuid4(),
        "business_id": uuid.uuid4(),
        "date": date(2025, 1, 1),
        "initial_hour": 23,
        "number_of_games":1,
        "is_reserved": False
    }
    available_date = AvailableDate(**data)
    # test
    available_dates_public = AvailableDatesPublic.from_private([available_date])
    # assert
    assert available_dates_public.count == 1
    available_date_public = available_dates_public.data[0]
    for key, value in data.items():
        if key == "id":
            continue
        assert getattr(available_date_public, key) == value