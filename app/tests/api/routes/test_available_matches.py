import uuid
from typing import Any

from httpx import AsyncClient
from starlette import status

from app.core.config import settings
from app.tests.utils.utils import (
    create_business_for_routes,
    create_padel_court_for_routes,
)


async def test_create_available_matches(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    owner_id = uuid.uuid4()

    new_business = await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": str(owner_id)},
        monkeypatch=monkeypatch,
    )
    assert new_business is not None

    court_name = "cancha 0"

    new_padel_court = await create_padel_court_for_routes(
        async_client=async_client,
        x_api_key_header=x_api_key_header,
        name=court_name,
        price_per_hour="150000",
        business_data=new_business,
        owner_id=owner_id,
    )

    assert new_padel_court is not None

    business_public_id = new_business.get("business_public_id")

    data_available_match = {
        "court_name": court_name,
        "business_public_id": business_public_id,
        "date": "2025-02-22",
        "initial_hour": "5",
        "n_matches": "5",
    }
    # test
    response = await async_client.post(
        f"{settings.API_V1_STR}/businesses/{business_public_id}/padel-courts/{court_name}/available-matches/",
        headers=x_api_key_header,
        json=data_available_match,
        params={
            "business_public_id": str(business_public_id),
            "user_id": str(owner_id),
            "court_name": str(court_name),
        },
    )
    # assert
    assert response is not None
    assert response.status_code == status.HTTP_201_CREATED
    result = response.json()
    assert result.get("count") == 5
    data = result.get("data")
    assert len(data) == 5
    sum_hours = 35
    for data_available_match in data:
        assert data_available_match.get("date") == "2025-02-22"
        available_match_initial_hour = int(data_available_match.get("initial_hour"))
        assert available_match_initial_hour >= 5 and available_match_initial_hour <= 9
        sum_hours -= available_match_initial_hour
        assert data_available_match.get("business_public_id") == business_public_id
        assert data_available_match.get("court_name") == court_name
    assert sum_hours == 0


async def test_create_available_matches_with_another_owner_id_returns_401(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    owner_id = uuid.uuid4()

    new_business = await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": str(owner_id)},
        monkeypatch=monkeypatch,
    )
    assert new_business is not None

    court_name = "cancha 0"

    new_padel_court = await create_padel_court_for_routes(
        async_client=async_client,
        x_api_key_header=x_api_key_header,
        name=court_name,
        price_per_hour="150000",
        business_data=new_business,
        owner_id=owner_id,
    )

    assert new_padel_court is not None

    business_public_id = new_business.get("business_public_id")

    data_available_match = {
        "court_name": court_name,
        "business_public_id": business_public_id,
        "date": "2025-02-22",
        "initial_hour": "5",
        "n_matches": "5",
    }
    # test
    response = await async_client.post(
        f"{settings.API_V1_STR}/businesses/{business_public_id}/padel-courts/{court_name}/available-matches/",
        headers=x_api_key_header,
        json=data_available_match,
        params={
            "business_public_id": str(business_public_id),
            "user_id": str(uuid.uuid4()),
            "court_name": str(court_name),
        },
    )
    # assert
    assert response is not None
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    content = response.json()
    assert content["detail"] == "User is not the owner"


async def test_create_available_matches_with_time_superposition_on_same_date_returns_409(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    owner_id = uuid.uuid4()

    new_business = await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": str(owner_id)},
        monkeypatch=monkeypatch,
    )
    assert new_business is not None

    court_name = "cancha 0"

    new_padel_court = await create_padel_court_for_routes(
        async_client=async_client,
        x_api_key_header=x_api_key_header,
        name=court_name,
        price_per_hour="150000",
        business_data=new_business,
        owner_id=owner_id,
    )

    assert new_padel_court is not None

    business_public_id = new_business.get("business_public_id")

    data_available_match = {
        "court_name": court_name,
        "business_public_id": business_public_id,
        "date": "2025-02-22",
        "initial_hour": "5",
        "n_matches": "5",
    }
    created_available_matches = await async_client.post(
        f"{settings.API_V1_STR}/businesses/{business_public_id}/padel-courts/{court_name}/available-matches/",
        headers=x_api_key_header,
        json=data_available_match,
        params={
            "business_public_id": str(business_public_id),
            "user_id": str(owner_id),
            "court_name": str(court_name),
        },
    )

    assert created_available_matches is not None

    data_available_match_new = {
        "court_name": court_name,
        "business_public_id": business_public_id,
        "date": "2025-02-22",
        "initial_hour": "7",
        "n_matches": "1",
    }
    # test
    response = await async_client.post(
        f"{settings.API_V1_STR}/businesses/{business_public_id}/padel-courts/{court_name}/available-matches/",
        headers=x_api_key_header,
        json=data_available_match_new,
        params={
            "business_public_id": str(business_public_id),
            "user_id": str(owner_id),
            "court_name": str(court_name),
        },
    )
    # assert
    assert response is not None
    assert response.status_code == status.HTTP_409_CONFLICT
    content = response.json()
    assert content["detail"] == "Available date already exists."


async def test_multiple_valid_create_available_matches(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    owner_id = uuid.uuid4()

    new_business = await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": str(owner_id)},
        monkeypatch=monkeypatch,
    )
    assert new_business is not None

    court_name = "cancha 0"

    new_padel_court = await create_padel_court_for_routes(
        async_client=async_client,
        x_api_key_header=x_api_key_header,
        name=court_name,
        price_per_hour="150000",
        business_data=new_business,
        owner_id=owner_id,
    )

    assert new_padel_court is not None

    business_public_id = new_business.get("business_public_id")
    data_available_match = {
        "court_name": court_name,
        "business_public_id": business_public_id,
        "date": "2025-02-22",
        "initial_hour": "5",
        "n_matches": "5",
    }
    created_available_matches = await async_client.post(
        f"{settings.API_V1_STR}/businesses/{business_public_id}/padel-courts/{court_name}/available-matches/",
        headers=x_api_key_header,
        json=data_available_match,
        params={
            "business_public_id": str(business_public_id),
            "user_id": str(owner_id),
            "court_name": str(court_name),
        },
    )
    assert created_available_matches is not None
    # test
    data_available_match_new_after = {
        "court_name": court_name,
        "business_public_id": business_public_id,
        "date": "2025-02-22",
        "initial_hour": "10",
        "n_matches": "3",
    }
    created_available_matches_after = await async_client.post(
        f"{settings.API_V1_STR}/businesses/{business_public_id}/padel-courts/{court_name}/available-matches/",
        headers=x_api_key_header,
        json=data_available_match_new_after,
        params={
            "business_public_id": str(business_public_id),
            "user_id": str(owner_id),
            "court_name": str(court_name),
        },
    )
    data_available_match_new_before = {
        "court_name": court_name,
        "business_public_id": business_public_id,
        "date": "2025-02-22",
        "initial_hour": "4",
        "n_matches": "1",
    }
    created_available_matches_before = await async_client.post(
        f"{settings.API_V1_STR}/businesses/{business_public_id}/padel-courts/{court_name}/available-matches/",
        headers=x_api_key_header,
        json=data_available_match_new_before,
        params={
            "business_public_id": str(business_public_id),
            "user_id": str(owner_id),
            "court_name": str(court_name),
        },
    )
    # assert
    assert created_available_matches_after is not None
    assert created_available_matches_before is not None
    assert created_available_matches.status_code == status.HTTP_201_CREATED
    assert created_available_matches_after.status_code == status.HTTP_201_CREATED
    assert created_available_matches_before.status_code == status.HTTP_201_CREATED
    assert created_available_matches.json().get("count") == 5
    assert created_available_matches_after.json().get("count") == 3
    assert created_available_matches_before.json().get("count") == 1


async def test_get_available_matches(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    owner_id = uuid.uuid4()

    new_business = await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": str(owner_id)},
        monkeypatch=monkeypatch,
    )
    assert new_business is not None

    court_name = "cancha 0"

    new_padel_court = await create_padel_court_for_routes(
        async_client=async_client,
        x_api_key_header=x_api_key_header,
        name=court_name,
        price_per_hour="150000",
        business_data=new_business,
        owner_id=owner_id,
    )

    assert new_padel_court is not None

    business_public_id = new_business.get("business_public_id")
    data_available_match = {
        "court_name": court_name,
        "business_public_id": business_public_id,
        "date": "2025-02-22",
        "initial_hour": "5",
        "n_matches": "5",
    }
    created_available_matches = await async_client.post(
        f"{settings.API_V1_STR}/businesses/{business_public_id}/padel-courts/{court_name}/available-matches/",
        headers=x_api_key_header,
        json=data_available_match,
        params={
            "business_public_id": str(business_public_id),
            "user_id": str(owner_id),
            "court_name": str(court_name),
        },
    )
    assert created_available_matches is not None
    # test
    parameters = {
        "court_name": str(court_name),
        "business_public_id": str(business_public_id),
        "date": str(data_available_match["date"]),
    }
    get_available_matches = await async_client.get(
        f"{settings.API_V1_STR}/businesses/{business_public_id}/padel-courts/{court_name}/available-matches/",
        headers=x_api_key_header,
        params=parameters,
    )
    # assert
    assert get_available_matches is not None
    assert get_available_matches.status_code == status.HTTP_200_OK
    get_result = get_available_matches.json()
    assert get_result.get("count") == 5

    data = get_result.get("data")
    assert len(data) == 5
    sum_hours = 35
    for data_available_match in data:
        assert data_available_match.get("date") == "2025-02-22"
        available_match_initial_hour = int(data_available_match.get("initial_hour"))
        assert available_match_initial_hour >= 5 and available_match_initial_hour <= 9
        sum_hours -= available_match_initial_hour
        assert data_available_match.get("business_public_id") == business_public_id
        assert data_available_match.get("court_name") == court_name
    assert sum_hours == 0


async def test_update_for_reserve_available_matches(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    owner_id = uuid.uuid4()

    new_business = await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": str(owner_id)},
        monkeypatch=monkeypatch,
    )
    assert new_business is not None

    court_name = "cancha 0"

    new_padel_court = await create_padel_court_for_routes(
        async_client=async_client,
        x_api_key_header=x_api_key_header,
        name=court_name,
        price_per_hour="150000",
        business_data=new_business,
        owner_id=owner_id,
    )

    assert new_padel_court is not None

    business_public_id = new_business.get("business_public_id")
    data_available_match = {
        "court_name": court_name,
        "business_public_id": business_public_id,
        "date": "2025-02-22",
        "initial_hour": "5",
        "n_matches": "5",
    }
    created_available_matches = await async_client.post(
        f"{settings.API_V1_STR}/businesses/{business_public_id}/padel-courts/{court_name}/available-matches/",
        headers=x_api_key_header,
        json=data_available_match,
        params={
            "business_public_id": str(business_public_id),
            "user_id": str(owner_id),
            "court_name": str(court_name),
        },
    )
    assert created_available_matches is not None
    # test
    reserve = await async_client.patch(
        f"{settings.API_V1_STR}/businesses/{business_public_id}/padel-courts/{court_name}/available-matches/",
        headers=x_api_key_header,
        params={
            "court_name": str(court_name),
            "business_public_id": str(business_public_id),
            "date": str(data_available_match["date"]),
            "hour": str(7),
        },
    )

    parameters = {
        "court_name": str(court_name),
        "business_public_id": str(business_public_id),
        "date": str(data_available_match["date"]),
    }
    get_available_matches = await async_client.get(
        f"{settings.API_V1_STR}/businesses/{business_public_id}/padel-courts/{court_name}/available-matches/",
        headers=x_api_key_header,
        params=parameters,
    )
    # assert
    assert reserve is not None
    assert reserve.status_code == status.HTTP_200_OK
    assert get_available_matches is not None
    assert get_available_matches.status_code == status.HTTP_200_OK
    get_result = get_available_matches.json()
    assert get_result.get("count") == 5
    print(reserve.json().keys())
    # assert reserve.json().get("is_reserved")
    assert reserve.json().get("reserve")


async def test_update_for_reserve_available_matches_with_inexistent_hour_returns_404(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    owner_id = uuid.uuid4()

    new_business = await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": str(owner_id)},
        monkeypatch=monkeypatch,
    )
    assert new_business is not None

    court_name = "cancha 0"

    new_padel_court = await create_padel_court_for_routes(
        async_client=async_client,
        x_api_key_header=x_api_key_header,
        name=court_name,
        price_per_hour="150000",
        business_data=new_business,
        owner_id=owner_id,
    )

    assert new_padel_court is not None

    business_public_id = new_business.get("business_public_id")
    data_available_match = {
        "court_name": court_name,
        "business_public_id": business_public_id,
        "date": "2025-02-22",
        "initial_hour": "5",
        "n_matches": "5",
    }
    created_available_matches = await async_client.post(
        f"{settings.API_V1_STR}/businesses/{business_public_id}/padel-courts/{court_name}/available-matches/",
        headers=x_api_key_header,
        json=data_available_match,
        params={
            "business_public_id": str(business_public_id),
            "user_id": str(owner_id),
            "court_name": str(court_name),
        },
    )
    assert created_available_matches is not None
    # test
    reserve = await async_client.patch(
        f"{settings.API_V1_STR}/businesses/{business_public_id}/padel-courts/{court_name}/available-matches/",
        headers=x_api_key_header,
        params={
            "court_name": str(court_name),
            "business_public_id": str(business_public_id),
            "date": str(data_available_match["date"]),
            "hour": str(1),
        },
    )
    # assert
    assert reserve is not None
    assert reserve.status_code == status.HTTP_404_NOT_FOUND
    content = reserve.json()
    assert content["detail"] == "Available match not found"


async def test_delete_all_available_matches_in_a_date(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    owner_id = uuid.uuid4()

    new_business = await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": str(owner_id)},
        monkeypatch=monkeypatch,
    )
    assert new_business is not None

    court_name = "cancha 0"

    new_padel_court = await create_padel_court_for_routes(
        async_client=async_client,
        x_api_key_header=x_api_key_header,
        name=court_name,
        price_per_hour="150000",
        business_data=new_business,
        owner_id=owner_id,
    )

    assert new_padel_court is not None

    business_public_id = new_business.get("business_public_id")
    data_available_match = {
        "court_name": court_name,
        "business_public_id": business_public_id,
        "date": "2025-02-22",
        "initial_hour": "5",
        "n_matches": "5",
    }
    created_available_matches = await async_client.post(
        f"{settings.API_V1_STR}/businesses/{business_public_id}/padel-courts/{court_name}/available-matches/",
        headers=x_api_key_header,
        json=data_available_match,
        params={
            "business_public_id": str(business_public_id),
            "user_id": str(owner_id),
            "court_name": str(court_name),
        },
    )
    assert created_available_matches is not None
    await async_client.patch(
        f"{settings.API_V1_STR}/businesses/{business_public_id}/padel-courts/{court_name}/available-matches/",
        headers=x_api_key_header,
        params={
            "court_name": str(court_name),
            "business_public_id": str(business_public_id),
            "date": str(data_available_match["date"]),
            "hour": str(7),
        },
    )
    # test
    response_delete = await async_client.delete(
        f"{settings.API_V1_STR}/businesses/{business_public_id}/padel-courts/{court_name}/available-matches/",
        headers=x_api_key_header,
        params={
            "court_name": str(court_name),
            "business_public_id": str(business_public_id),
            "user_id": str(owner_id),
            "date": str(data_available_match["date"]),
        },
    )
    parameters = {
        "court_name": str(court_name),
        "business_public_id": str(business_public_id),
        "date": str(data_available_match["date"]),
    }
    get_available_matches = await async_client.get(
        f"{settings.API_V1_STR}/businesses/{business_public_id}/padel-courts/{court_name}/available-matches/",
        headers=x_api_key_header,
        params=parameters,
    )
    # assert
    assert response_delete is not None
    assert response_delete.status_code == status.HTTP_204_NO_CONTENT
    assert get_available_matches is not None
    assert get_available_matches.status_code == status.HTTP_200_OK
    get_result = get_available_matches.json()
    assert get_result.get("count") == 0


async def test_delete_available_matches_with_not_authorized_owner_user_id_returns_401(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    owner_id = uuid.uuid4()

    new_business = await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": str(owner_id)},
        monkeypatch=monkeypatch,
    )
    assert new_business is not None

    court_name = "cancha 0"

    new_padel_court = await create_padel_court_for_routes(
        async_client=async_client,
        x_api_key_header=x_api_key_header,
        name=court_name,
        price_per_hour="150000",
        business_data=new_business,
        owner_id=owner_id,
    )

    assert new_padel_court is not None

    business_public_id = new_business.get("business_public_id")
    data_available_match = {
        "court_name": court_name,
        "business_public_id": business_public_id,
        "date": "2025-02-22",
        "initial_hour": "5",
        "n_matches": "5",
    }
    created_available_matches = await async_client.post(
        f"{settings.API_V1_STR}/businesses/{business_public_id}/padel-courts/{court_name}/available-matches/",
        headers=x_api_key_header,
        json=data_available_match,
        params={
            "business_public_id": str(business_public_id),
            "user_id": str(owner_id),
            "court_name": str(court_name),
        },
    )
    assert created_available_matches is not None
    await async_client.patch(
        f"{settings.API_V1_STR}/businesses/{business_public_id}/padel-courts/{court_name}/available-matches/",
        headers=x_api_key_header,
        params={
            "court_name": str(court_name),
            "business_public_id": str(business_public_id),
            "date": str(data_available_match["date"]),
            "hour": str(7),
        },
    )
    # test
    response_delete = await async_client.delete(
        f"{settings.API_V1_STR}/businesses/{business_public_id}/padel-courts/{court_name}/available-matches/",
        headers=x_api_key_header,
        params={
            "court_name": str(court_name),
            "business_public_id": str(business_public_id),
            "user_id": str(uuid.uuid4()),
            "date": str(data_available_match["date"]),
        },
    )
    # assert
    assert response_delete is not None
    assert response_delete.status_code == status.HTTP_401_UNAUTHORIZED
    content = response_delete.json()
    assert content["detail"] == "User is not the owner"
