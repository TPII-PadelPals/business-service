import uuid

from httpx import AsyncClient
from starlette import status

from app.core.config import settings
from app.tests.utils.utils import _create_business, _create_padel_court


async def test_create_available_dates(
        async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    owner_id = uuid.uuid4()

    new_business = await _create_business(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": owner_id},
    )
    assert new_business is not None

    court_name = str("cancha 0")

    new_padel_court = await _create_padel_court(
        async_client=async_client,
        x_api_key_header=x_api_key_header,
        name=court_name,
        price_per_hour="150000",
        business_data=new_business,
        owner_id=owner_id,
    )

    assert new_padel_court is not None

    business_id = new_business.get("id")

    data_available_date = {
        "court_name": court_name,
        "business_id": business_id,
        "date": "2025-02-22",
        "initial_hour": "5",
        "number_of_games":"5",
    }
    # test
    response = await async_client.post(
        f"{settings.API_V1_STR}/padel-courts-available-date/",
        headers=x_api_key_header,
        json=data_available_date,
        params={"business_id": str(business_id), "user_id": owner_id, "court_name": str(court_name)},
    )
    # assert
    assert response is not None
    assert response.status_code == status.HTTP_201_CREATED
    result = response.json()
    assert result.get("count") == 5
    assert len(result.get("data")) == 5

async def test_create_available_dates_not_owner_401(
        async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    owner_id = uuid.uuid4()

    new_business = await _create_business(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": owner_id},
    )
    assert new_business is not None

    court_name = str("cancha 0")

    new_padel_court = await _create_padel_court(
        async_client=async_client,
        x_api_key_header=x_api_key_header,
        name=court_name,
        price_per_hour="150000",
        business_data=new_business,
        owner_id=owner_id,
    )

    assert new_padel_court is not None

    business_id = new_business.get("id")

    data_available_date = {
        "court_name": court_name,
        "business_id": business_id,
        "date": "2025-02-22",
        "initial_hour": "5",
        "number_of_games":"5",
    }
    # test
    response = await async_client.post(
        f"{settings.API_V1_STR}/padel-courts-available-date/",
        headers=x_api_key_header,
        json=data_available_date,
        params={"business_id": str(business_id), "user_id": uuid.uuid4(), "court_name": str(court_name)},
    )
    # assert
    assert response is not None
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


async def test_invalid_create_available_dates_409_crate_over_time(
        async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    owner_id = uuid.uuid4()

    new_business = await _create_business(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": owner_id},
    )
    assert new_business is not None

    court_name = str("cancha 0")

    new_padel_court = await _create_padel_court(
        async_client=async_client,
        x_api_key_header=x_api_key_header,
        name=court_name,
        price_per_hour="150000",
        business_data=new_business,
        owner_id=owner_id,
    )

    assert new_padel_court is not None

    business_id = new_business.get("id")

    data_available_date = {
        "court_name": court_name,
        "business_id": business_id,
        "date": "2025-02-22",
        "initial_hour": "5",
        "number_of_games":"5",
    }
    created_available_days = await async_client.post(
        f"{settings.API_V1_STR}/padel-courts-available-date/",
        headers=x_api_key_header,
        json=data_available_date,
        params={"business_id": str(business_id), "user_id": owner_id, "court_name": str(court_name)},
    )

    assert created_available_days is not None

    data_available_date_new = {
        "court_name": court_name,
        "business_id": business_id,
        "date": "2025-02-22",
        "initial_hour": "7",
        "number_of_games":"1",
    }
    # test
    response = await async_client.post(
        f"{settings.API_V1_STR}/padel-courts-available-date/",
        headers=x_api_key_header,
        json=data_available_date_new,
        params={"business_id": str(business_id), "user_id": owner_id, "court_name": str(court_name)},
    )
    # assert
    assert response is not None
    assert response.status_code == status.HTTP_409_CONFLICT


async def test_multiple_valid_create_available_dates(
        async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    owner_id = uuid.uuid4()

    new_business = await _create_business(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": owner_id},
    )
    assert new_business is not None

    court_name = str("cancha 0")

    new_padel_court = await _create_padel_court(
        async_client=async_client,
        x_api_key_header=x_api_key_header,
        name=court_name,
        price_per_hour="150000",
        business_data=new_business,
        owner_id=owner_id,
    )

    assert new_padel_court is not None

    business_id = new_business.get("id")
    data_available_date = {
        "court_name": court_name,
        "business_id": business_id,
        "date": "2025-02-22",
        "initial_hour": "5",
        "number_of_games":"5",
    }
    created_available_days = await async_client.post(
        f"{settings.API_V1_STR}/padel-courts-available-date/",
        headers=x_api_key_header,
        json=data_available_date,
        params={"business_id": str(business_id), "user_id": owner_id, "court_name": str(court_name)},
    )
    assert created_available_days is not None
    # test
    data_available_date_new_after = {
        "court_name": court_name,
        "business_id": business_id,
        "date": "2025-02-22",
        "initial_hour": "10",
        "number_of_games":"3",
    }
    created_available_days_after = await async_client.post(
        f"{settings.API_V1_STR}/padel-courts-available-date/",
        headers=x_api_key_header,
        json=data_available_date_new_after,
        params={"business_id": str(business_id), "user_id": owner_id, "court_name": str(court_name)},
    )
    data_available_date_new_before = {
        "court_name": court_name,
        "business_id": business_id,
        "date": "2025-02-22",
        "initial_hour": "4",
        "number_of_games":"1",
    }
    created_available_days_before = await async_client.post(
        f"{settings.API_V1_STR}/padel-courts-available-date/",
        headers=x_api_key_header,
        json=data_available_date_new_before,
        params={"business_id": str(business_id), "user_id": owner_id, "court_name": str(court_name)},
    )
    # assert
    assert created_available_days_after is not None
    assert created_available_days_before is not None
    assert created_available_days.status_code == status.HTTP_201_CREATED
    assert created_available_days_after.status_code == status.HTTP_201_CREATED
    assert created_available_days_before.status_code == status.HTTP_201_CREATED
    assert created_available_days.json().get("count") == 5
    assert created_available_days_after.json().get("count") == 3
    assert created_available_days_before.json().get("count") == 1


async def test_get_available_dates(
        async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    owner_id = uuid.uuid4()

    new_business = await _create_business(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": owner_id},
    )
    assert new_business is not None

    court_name = str("cancha 0")

    new_padel_court = await _create_padel_court(
        async_client=async_client,
        x_api_key_header=x_api_key_header,
        name=court_name,
        price_per_hour="150000",
        business_data=new_business,
        owner_id=owner_id,
    )

    assert new_padel_court is not None

    business_id = new_business.get("id")
    data_available_date = {
        "court_name": court_name,
        "business_id": business_id,
        "date": "2025-02-22",
        "initial_hour": "5",
        "number_of_games":"5",
    }
    created_available_days = await async_client.post(
        f"{settings.API_V1_STR}/padel-courts-available-date/",
        headers=x_api_key_header,
        json=data_available_date,
        params={"business_id": str(business_id), "user_id": owner_id, "court_name": str(court_name)},
    )
    assert created_available_days is not None
    # test
    parameters = {
        "court_name": str(court_name),
        "business_id": str(business_id),
        "date": str(data_available_date["date"])
    }
    get_available_days = await async_client.get(
        f"{settings.API_V1_STR}/padel-courts-available-date/",
        headers=x_api_key_header,
        params=parameters,
    )
    # assert
    assert get_available_days is not None
    assert get_available_days.status_code == status.HTTP_200_OK
    get_result = get_available_days.json()
    assert get_result.get("count") == 5


async def test_update_for_reserve_available_dates(
        async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    owner_id = uuid.uuid4()

    new_business = await _create_business(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": owner_id},
    )
    assert new_business is not None

    court_name = str("cancha 0")

    new_padel_court = await _create_padel_court(
        async_client=async_client,
        x_api_key_header=x_api_key_header,
        name=court_name,
        price_per_hour="150000",
        business_data=new_business,
        owner_id=owner_id,
    )

    assert new_padel_court is not None

    business_id = new_business.get("id")
    data_available_date = {
        "court_name": court_name,
        "business_id": business_id,
        "date": "2025-02-22",
        "initial_hour": "5",
        "number_of_games":"5",
    }
    created_available_days = await async_client.post(
        f"{settings.API_V1_STR}/padel-courts-available-date/",
        headers=x_api_key_header,
        json=data_available_date,
        params={"business_id": str(business_id), "user_id": owner_id, "court_name": str(court_name)},
    )
    assert created_available_days is not None
    # test
    reserve = await async_client.patch(
        f"{settings.API_V1_STR}/padel-courts-available-date/",
        headers=x_api_key_header,
        params={
            "court_name": str(court_name),
            "business_id": str(business_id),
            "date": str(data_available_date["date"]),
            "hour": str(7)
        },
    )

    parameters = {
        "court_name": str(court_name),
        "business_id": str(business_id),
        "date": str(data_available_date["date"])
    }
    get_available_days = await async_client.get(
        f"{settings.API_V1_STR}/padel-courts-available-date/",
        headers=x_api_key_header,
        params=parameters,
    )
    # assert
    assert reserve is not None
    assert reserve.status_code == status.HTTP_200_OK
    assert get_available_days is not None
    assert get_available_days.status_code == status.HTTP_200_OK
    get_result = get_available_days.json()
    assert get_result.get("count") == 5
    assert reserve.json().get("is_reserved") == True


async def test_update_for_reserve_available_dates_whit_invalid_hour(
        async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    owner_id = uuid.uuid4()

    new_business = await _create_business(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": owner_id},
    )
    assert new_business is not None

    court_name = str("cancha 0")

    new_padel_court = await _create_padel_court(
        async_client=async_client,
        x_api_key_header=x_api_key_header,
        name=court_name,
        price_per_hour="150000",
        business_data=new_business,
        owner_id=owner_id,
    )

    assert new_padel_court is not None

    business_id = new_business.get("id")
    data_available_date = {
        "court_name": court_name,
        "business_id": business_id,
        "date": "2025-02-22",
        "initial_hour": "5",
        "number_of_games":"5",
    }
    created_available_days = await async_client.post(
        f"{settings.API_V1_STR}/padel-courts-available-date/",
        headers=x_api_key_header,
        json=data_available_date,
        params={"business_id": str(business_id), "user_id": owner_id, "court_name": str(court_name)},
    )
    assert created_available_days is not None
    # test
    reserve = await async_client.patch(
        f"{settings.API_V1_STR}/padel-courts-available-date/",
        headers=x_api_key_header,
        params={
            "court_name": str(court_name),
            "business_id": str(business_id),
            "date": str(data_available_date["date"]),
            "hour": str(1)
        },
    )
    # assert
    assert reserve is not None
    assert reserve.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_all_available_dates_in_a_date(
        async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    owner_id = uuid.uuid4()

    new_business = await _create_business(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": owner_id},
    )
    assert new_business is not None

    court_name = str("cancha 0")

    new_padel_court = await _create_padel_court(
        async_client=async_client,
        x_api_key_header=x_api_key_header,
        name=court_name,
        price_per_hour="150000",
        business_data=new_business,
        owner_id=owner_id,
    )

    assert new_padel_court is not None

    business_id = new_business.get("id")
    data_available_date = {
        "court_name": court_name,
        "business_id": business_id,
        "date": "2025-02-22",
        "initial_hour": "5",
        "number_of_games":"5",
    }
    created_available_days = await async_client.post(
        f"{settings.API_V1_STR}/padel-courts-available-date/",
        headers=x_api_key_header,
        json=data_available_date,
        params={"business_id": str(business_id), "user_id": owner_id, "court_name": str(court_name)},
    )
    assert created_available_days is not None
    await async_client.patch(
        f"{settings.API_V1_STR}/padel-courts-available-date/",
        headers=x_api_key_header,
        params={
            "court_name": str(court_name),
            "business_id": str(business_id),
            "date": str(data_available_date["date"]),
            "hour": str(7)
        },
    )
    # test
    response_delete = await async_client.delete(
        f"{settings.API_V1_STR}/padel-courts-available-date/",
        headers=x_api_key_header,
        params={
            "court_name": str(court_name),
            "business_id": str(business_id),
            "user_id": str(owner_id),
            "date": str(data_available_date["date"])
        },
    )
    parameters = {
        "court_name": str(court_name),
        "business_id": str(business_id),
        "date": str(data_available_date["date"])
    }
    get_available_days = await async_client.get(
        f"{settings.API_V1_STR}/padel-courts-available-date/",
        headers=x_api_key_header,
        params=parameters,
    )
    # assert
    assert response_delete is not None
    assert response_delete.status_code == status.HTTP_204_NO_CONTENT
    assert get_available_days is not None
    assert get_available_days.status_code == status.HTTP_200_OK
    get_result = get_available_days.json()
    assert get_result.get("count") == 0


async def test_delete_available_dates_no_owner(
        async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    owner_id = uuid.uuid4()

    new_business = await _create_business(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": owner_id},
    )
    assert new_business is not None

    court_name = str("cancha 0")

    new_padel_court = await _create_padel_court(
        async_client=async_client,
        x_api_key_header=x_api_key_header,
        name=court_name,
        price_per_hour="150000",
        business_data=new_business,
        owner_id=owner_id,
    )

    assert new_padel_court is not None

    business_id = new_business.get("id")
    data_available_date = {
        "court_name": court_name,
        "business_id": business_id,
        "date": "2025-02-22",
        "initial_hour": "5",
        "number_of_games":"5",
    }
    created_available_days = await async_client.post(
        f"{settings.API_V1_STR}/padel-courts-available-date/",
        headers=x_api_key_header,
        json=data_available_date,
        params={"business_id": str(business_id), "user_id": owner_id, "court_name": str(court_name)},
    )
    assert created_available_days is not None
    await async_client.patch(
        f"{settings.API_V1_STR}/padel-courts-available-date/",
        headers=x_api_key_header,
        params={
            "court_name": str(court_name),
            "business_id": str(business_id),
            "date": str(data_available_date["date"]),
            "hour": str(7)
        },
    )
    # test
    response_delete = await async_client.delete(
        f"{settings.API_V1_STR}/padel-courts-available-date/",
        headers=x_api_key_header,
        params={
            "court_name": str(court_name),
            "business_id": str(business_id),
            "user_id": str(uuid.uuid4()),
            "date": str(data_available_date["date"])
        },
    )
    # assert
    assert response_delete is not None
    assert response_delete.status_code == status.HTTP_401_UNAUTHORIZED