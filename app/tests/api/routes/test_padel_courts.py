import uuid
from typing import Any

from httpx import AsyncClient

from app.core.config import settings
from app.tests.utils.utils import (
    create_business_for_routes,
    create_padel_court_for_routes,
)


async def test_create_padel_court_with_existing_business(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    owner_id = uuid.uuid4()

    new_business = await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": owner_id},
        monkeypatch=monkeypatch,
    )

    padel_court_data = {"name": "Cancha 1", "price_per_hour": "15000.00"}

    response = await async_client.post(
        f"{settings.API_V1_STR}/padel-courts/",
        headers=x_api_key_header,
        json=padel_court_data,
        params={
            "business_public_id": new_business["business_public_id"],
            "owner_id": owner_id,
        },
    )

    assert response.status_code == 201
    content = response.json()

    assert content["name"] == padel_court_data["name"]
    assert content["price_per_hour"] == padel_court_data["price_per_hour"]
    assert "business_public_id" in content
    assert "court_public_id" in content


async def test_create_padel_court_with_nonexisting_business_public_id_returns_error(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    owner_id = uuid.uuid4()
    nonexisting_business_public_id = uuid.uuid4()

    _new_business = await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": owner_id},
        monkeypatch=monkeypatch,
    )

    padel_court_data = {"name": "Cancha 1", "price_per_hour": "1500000"}

    response = await async_client.post(
        f"{settings.API_V1_STR}/padel-courts/",
        headers=x_api_key_header,
        json=padel_court_data,
        params={
            "business_public_id": nonexisting_business_public_id,
            "owner_id": owner_id,
        },
    )

    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Business not found"


async def test_create_padel_court_with_unauthorized_owner_id_returns_error(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    owner_id = uuid.uuid4()

    new_business = await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": owner_id},
        monkeypatch=monkeypatch,
    )

    unauthorized_owner_id = uuid.uuid4()

    padel_court_data = {"name": "Cancha 20", "price_per_hour": "30000"}

    response = await async_client.post(
        f"{settings.API_V1_STR}/padel-courts/",
        headers=x_api_key_header,
        json=padel_court_data,
        params={
            "business_public_id": new_business["business_public_id"],
            "owner_id": unauthorized_owner_id,
        },
    )

    assert response.status_code == 403
    content = response.json()
    assert content["detail"] == "Not enough permissions"


async def test_get_all_padel_courts(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    owner_id = uuid.uuid4()

    business1 = await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="API Court Business 1",
        location="API Court Location 1",
        parameters={"owner_id": str(owner_id)},
        monkeypatch=monkeypatch,
    )

    business2 = await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="API Court Business 2",
        location="API Court Location 2",
        parameters={"owner_id": str(owner_id)},
        monkeypatch=monkeypatch,
    )

    await create_padel_court_for_routes(
        async_client=async_client,
        x_api_key_header=x_api_key_header,
        name="API Court A",
        price_per_hour="100.00",
        business_data=business1,
        owner_id=owner_id,
    )

    await create_padel_court_for_routes(
        async_client=async_client,
        x_api_key_header=x_api_key_header,
        name="API Court B",
        price_per_hour="150.00",
        business_data=business2,
        owner_id=owner_id,
    )

    response = await async_client.get(
        f"{settings.API_V1_STR}/padel-courts/",
        headers=x_api_key_header,
    )

    assert response.status_code == 200
    content = response.json()
    assert "data" in content
    assert "count" in content
    assert content["count"] >= 2

    court_names = [c["name"] for c in content["data"]]
    assert "API Court A" in court_names
    assert "API Court B" in court_names


async def test_get_padel_courts_filtered_by_business(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    owner_id = uuid.uuid4()

    business1 = await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Filter Court Business 1",
        location="Filter Court Location 1",
        parameters={"owner_id": str(owner_id)},
        monkeypatch=monkeypatch,
    )

    business2 = await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Filter Court Business 2",
        location="Filter Court Location 2",
        parameters={"owner_id": str(owner_id)},
        monkeypatch=monkeypatch,
    )

    await create_padel_court_for_routes(
        async_client=async_client,
        x_api_key_header=x_api_key_header,
        name="Filter Court X",
        price_per_hour="100.00",
        business_data=business1,
        owner_id=owner_id,
    )

    await create_padel_court_for_routes(
        async_client=async_client,
        x_api_key_header=x_api_key_header,
        name="Filter Court Y",
        price_per_hour="150.00",
        business_data=business2,
        owner_id=owner_id,
    )

    response = await async_client.get(
        f"{settings.API_V1_STR}/padel-courts/",
        headers=x_api_key_header,
        params={
            "business_public_id": business1["business_public_id"],
            "user_id": str(owner_id),
        },
    )

    assert response.status_code == 200
    content = response.json()

    for court in content["data"]:
        assert court["business_public_id"] == business1["business_public_id"]

    court_names = [c["name"] for c in content["data"]]
    assert "Filter Court X" in court_names
    assert "Filter Court Y" not in court_names


async def test_get_padel_courts_with_pagination(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    owner_id = uuid.uuid4()
    business = await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Pagination Court Business",
        location="Pagination Court Location",
        parameters={"owner_id": str(owner_id)},
        monkeypatch=monkeypatch,
    )

    for i in range(1, 6):
        await create_padel_court_for_routes(
            async_client=async_client,
            x_api_key_header=x_api_key_header,
            name=f"Pagination Court {i}",
            price_per_hour=str(100.00 + i * 10),
            business_data=business,
            owner_id=owner_id,
        )

    response_page1 = await async_client.get(
        f"{settings.API_V1_STR}/padel-courts/",
        headers=x_api_key_header,
        params={
            "business_public_id": business["business_public_id"],
            "user_id": str(owner_id),
            "skip": "0",
            "limit": "2",
        },
    )

    response_page2 = await async_client.get(
        f"{settings.API_V1_STR}/padel-courts/",
        headers=x_api_key_header,
        params={
            "business_public_id": business["business_public_id"],
            "user_id": str(owner_id),
            "skip": "2",
            "limit": "2",
        },
    )

    assert response_page1.status_code == 200
    content_page1 = response_page1.json()
    assert len(content_page1["data"]) == 2

    assert response_page2.status_code == 200
    content_page2 = response_page2.json()
    assert len(content_page2["data"]) == 2

    page1_ids = [c["court_public_id"] for c in content_page1["data"]]
    page2_ids = [c["court_public_id"] for c in content_page2["data"]]
    assert not any(id in page1_ids for id in page2_ids)


async def test_update_padel_court(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    owner_id = uuid.uuid4()
    new_business = await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": owner_id},
        monkeypatch=monkeypatch,
    )
    padel_court_data = {"name": "Cancha 1", "price_per_hour": "15000.00"}
    response = await async_client.post(
        f"{settings.API_V1_STR}/padel-courts/",
        headers=x_api_key_header,
        json=padel_court_data,
        params={
            "business_public_id": new_business["business_public_id"],
            "owner_id": str(owner_id),
        },
    )
    assert response.status_code == 201
    content = response.json()
    assert content["name"] == padel_court_data["name"]
    assert content["price_per_hour"] == padel_court_data["price_per_hour"]

    update_court_data = {"name": "Cancha sol", "price_per_hour": "25000.00"}
    update_response = await async_client.patch(
        f"{settings.API_V1_STR}/padel-courts/{content['court_public_id']}",
        headers=x_api_key_header,
        json=update_court_data,
        params={
            "business_public_id": new_business["business_public_id"],
            "user_id": str(owner_id),
        },
    )

    assert update_response.status_code == 200
    update_content = update_response.json()
    assert update_content["name"] == update_court_data["name"]
    assert update_content["price_per_hour"] == update_court_data["price_per_hour"]
    assert update_content["business_public_id"] == content["business_public_id"]
    assert update_content["court_public_id"] == content["court_public_id"]


async def test_update_padel_court_unauthorized(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    owner_id = uuid.uuid4()
    new_business = await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": owner_id},
        monkeypatch=monkeypatch,
    )
    padel_court_data = {"name": "Cancha 1", "price_per_hour": "15000.00"}
    response = await async_client.post(
        f"{settings.API_V1_STR}/padel-courts/",
        headers=x_api_key_header,
        json=padel_court_data,
        params={
            "business_public_id": new_business["business_public_id"],
            "owner_id": str(owner_id),
        },
    )
    assert response.status_code == 201
    content = response.json()
    assert content["name"] == padel_court_data["name"]
    assert content["price_per_hour"] == padel_court_data["price_per_hour"]

    update_court_data = {"name": "Cancha sol", "price_per_hour": "25000.00"}
    update_response = await async_client.patch(
        f"{settings.API_V1_STR}/padel-courts/{content['court_public_id']}",
        headers=x_api_key_header,
        json=update_court_data,
        params={
            "business_public_id": new_business["business_public_id"],
            "user_id": str(uuid.uuid4()),
        },
    )

    assert update_response.status_code == 401
    assert update_response.json().get("detail") == "User is not the owner"


async def test_update_padel_court_not_court(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    owner_id = uuid.uuid4()
    new_business = await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": owner_id},
        monkeypatch=monkeypatch,
    )
    court_public_id = uuid.uuid4()
    update_court_data = {"name": "Cancha sol", "price_per_hour": "25000.00"}
    update_response = await async_client.patch(
        f"{settings.API_V1_STR}/padel-courts/{court_public_id}",
        headers=x_api_key_header,
        json=update_court_data,
        params={
            "business_public_id": new_business["business_public_id"],
            "user_id": str(owner_id),
        },
    )

    assert update_response.status_code == 404
    assert update_response.json().get("detail") == "Padel court not found"


async def test_update_padel_court_not_business(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
) -> None:
    owner_id = uuid.uuid4()
    new_business = await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": owner_id},
        monkeypatch=monkeypatch,
    )
    padel_court_data = {"name": "Cancha 1", "price_per_hour": "15000.00"}
    response = await async_client.post(
        f"{settings.API_V1_STR}/padel-courts/",
        headers=x_api_key_header,
        json=padel_court_data,
        params={
            "business_public_id": new_business["business_public_id"],
            "owner_id": str(owner_id),
        },
    )
    assert response.status_code == 201
    content = response.json()
    assert content["name"] == padel_court_data["name"]
    assert content["price_per_hour"] == padel_court_data["price_per_hour"]

    update_court_data = {"name": "Cancha sol", "price_per_hour": "25000.00"}
    update_response = await async_client.patch(
        f"{settings.API_V1_STR}/padel-courts/{content['court_public_id']}",
        headers=x_api_key_header,
        json=update_court_data,
        params={
            "business_public_id": uuid.uuid4(),
            "user_id": str(owner_id),
        },
    )

    assert update_response.status_code == 404
    assert update_response.json().get("detail") == "Business not found"
