import random
import string
import uuid
from typing import Any

from httpx import AsyncClient

from app.core.config import settings
from app.services.google_service import GoogleService


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def get_x_api_key_header() -> dict[str, str]:
    headers = {"x-api-key": f"{settings.API_KEY}"}
    return headers


async def create_business_for_routes(
    async_client: AsyncClient,
    x_api_key,
    name: str,
    location: str,
    parameters: dict[str, str | int | uuid.UUID],
    monkeypatch: Any,
) -> dict[str, str]:
    GET_COORDS_RESULT = (0.4, 0.3)

    async def mock_get_coordinates(_self: Any, _: str) -> tuple[float, float]:
        return GET_COORDS_RESULT

    monkeypatch.setattr(GoogleService, "get_coordinates", mock_get_coordinates)

    business_data = {"name": name, "location": location}
    response = await async_client.post(
        f"{settings.API_V1_STR}/businesses/",
        headers=x_api_key,
        json=business_data,
        params=parameters,
    )
    return dict(response.json())


async def create_padel_court_for_routes(
    async_client: AsyncClient,
    x_api_key_header: dict[str, str],
    name: str,
    price_per_hour: str,
    business_data: dict[str, str],
    owner_id: uuid.UUID,
) -> dict[str, str]:
    padel_court_data = {"name": name, "price_per_hour": price_per_hour}

    response = await async_client.post(
        f"{settings.API_V1_STR}/padel-courts/",
        headers=x_api_key_header,
        json=padel_court_data,
        params={"business_id": str(business_data["id"]), "owner_id": str(owner_id)},
    )
    return dict(response.json())
