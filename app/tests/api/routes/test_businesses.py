import uuid
from http import HTTPStatus
from typing import Any

from httpx import AsyncClient

from app.core.config import settings
from app.services.google_service import GoogleService
from app.utilities.exceptions import (
    ExternalServiceException,
    ExternalServiceInvalidLocalizationException,
)


async def test_create_business(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
):
    GET_COORDS_RESULT = (0.4, 0.3)

    async def mock_get_coordinates(_self: Any, _: str) -> tuple[float, float]:
        return GET_COORDS_RESULT

    monkeypatch.setattr(GoogleService, "get_coordinates", mock_get_coordinates)

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


async def test_create_business_raise_invalid_conection_whit_google(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
):
    async def mock_get_coordinates(_self: Any, _: str) -> tuple[float, float]:
        raise ExternalServiceException(
            service_name="google-address",
            detail="Failed to fetch coordinates from Google",
        )

    monkeypatch.setattr(GoogleService, "get_coordinates", mock_get_coordinates)

    owner_id = uuid.uuid4()
    business_data = {"name": "Foo", "location": "Av. Belgrano 3450"}
    response = await async_client.post(
        f"{settings.API_V1_STR}/businesses/",
        headers=x_api_key_header,
        json=business_data,
        params={"owner_id": str(owner_id)},
    )
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR


async def test_create_business_raise_invalid_location(
    async_client: AsyncClient, x_api_key_header: dict[str, str], monkeypatch: Any
):
    async def mock_get_coordinates(_self: Any, _: str) -> tuple[float, float]:
        raise ExternalServiceInvalidLocalizationException(service_name="google-address")

    monkeypatch.setattr(GoogleService, "get_coordinates", mock_get_coordinates)

    owner_id = uuid.uuid4()
    business_data = {"name": "Foo", "location": "Av. Belgrano 3450"}
    response = await async_client.post(
        f"{settings.API_V1_STR}/businesses/",
        headers=x_api_key_header,
        json=business_data,
        params={"owner_id": str(owner_id)},
    )
    print(response)
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
