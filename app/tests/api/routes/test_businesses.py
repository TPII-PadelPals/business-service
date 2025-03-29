import uuid
from http import HTTPStatus

from httpx import AsyncClient

from app.core.config import settings
from app.tests.utils.utils import create_business_for_routes


async def test_create_business(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
):
    owner_id = uuid.uuid4()
    business_data = {"name": "Foo", "location": "Av. Belgrano 3450"}
    response = await async_client.post(
        f"{settings.API_V1_STR}/businesses/",
        headers=x_api_key_header,
        json=business_data,
        params={"owner_id": str(owner_id)},
    )
    assert response.status_code == 201
    content = response.json()
    assert content["name"] == business_data["name"]
    assert content["location"] == business_data["location"]
    assert "id" in content
    assert "owner_id" in content


async def test_create_business_without_owner_id(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
):
    business_data = {"name": "Foo", "location": "Av. Belgrano 3450"}

    response = await async_client.post(
        f"{settings.API_V1_STR}/businesses/",
        headers=x_api_key_header,
        json=business_data,
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    content = response.json()
    assert "detail" in content

    assert any(
        item["loc"] == ["query", "owner_id"] and item["msg"] == "Field required"
        for item in content["detail"]
    )


async def test_get_all_businesses(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    owner_id = uuid.uuid4()

    await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="API Test Business 1",
        location="API Location 1",
        parameters={"owner_id": str(owner_id)},
    )

    await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="API Test Business 2",
        location="API Location 2",
        parameters={"owner_id": str(owner_id)},
    )

    response = await async_client.get(
        f"{settings.API_V1_STR}/businesses/",
        headers=x_api_key_header,
    )

    assert response.status_code == 200
    content = response.json()
    assert "data" in content
    assert "count" in content
    assert content["count"] >= 2

    business_names = [b["name"] for b in content["data"]]
    assert "API Test Business 1" in business_names
    assert "API Test Business 2" in business_names


async def test_get_businesses_filtered_by_owner(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    owner1_id = uuid.uuid4()
    owner2_id = uuid.uuid4()

    await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Owner1 API Business",
        location="Owner1 Location",
        parameters={"owner_id": str(owner1_id)},
    )

    await create_business_for_routes(
        async_client=async_client,
        x_api_key=x_api_key_header,
        name="Owner2 API Business",
        location="Owner2 Location",
        parameters={"owner_id": str(owner2_id)},
    )

    response = await async_client.get(
        f"{settings.API_V1_STR}/businesses/",
        headers=x_api_key_header,
        params={"owner_id": str(owner1_id)},
    )

    assert response.status_code == 200
    content = response.json()

    for business in content["data"]:
        assert business["owner_id"] == str(owner1_id)

    business_names = [b["name"] for b in content["data"]]
    assert "Owner2 API Business" not in business_names


async def test_get_businesses_with_pagination(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    owner_id = uuid.uuid4()
    for i in range(1, 6):
        await create_business_for_routes(
            async_client=async_client,
            x_api_key=x_api_key_header,
            name=f"Pagination API Business {i}",
            location=f"Pagination Location {i}",
            parameters={"owner_id": str(owner_id)},
        )

    response_page1 = await async_client.get(
        f"{settings.API_V1_STR}/businesses/",
        headers=x_api_key_header,
        params={"skip": "0", "limit": "2"},
    )

    response_page2 = await async_client.get(
        f"{settings.API_V1_STR}/businesses/",
        headers=x_api_key_header,
        params={"skip": "2", "limit": "2"},
    )

    assert response_page1.status_code == 200
    content_page1 = response_page1.json()
    assert len(content_page1["data"]) == 2

    assert response_page2.status_code == 200
    content_page2 = response_page2.json()
    assert len(content_page2["data"]) == 2

    page1_ids = [b["id"] for b in content_page1["data"]]
    page2_ids = [b["id"] for b in content_page2["data"]]
    assert not any(id in page1_ids for id in page2_ids)
