import uuid
from http import HTTPStatus

from httpx import AsyncClient

from app.core.config import settings


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
