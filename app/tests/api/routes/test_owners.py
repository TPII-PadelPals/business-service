import uuid

from httpx import AsyncClient

from app.core.config import settings


async def test_create_owner(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    owner_id = str(uuid.uuid4())
    owner_password = "<PASSWORD>"
    owner_data = {"user_public_id": owner_id, "password_hash": owner_password}
    response = await async_client.post(
        f"{settings.API_V1_STR}/owner/",
        headers=x_api_key_header,
        json=owner_data,
        params={"owner_id": str(owner_id)},
    )
    assert response.status_code == 201
    content = response.json()
    assert content["user_public_id"] == owner_id
    assert content["password_hash"] == owner_password


async def test_create_owner_already_exist_raise_error_409(
    async_client: AsyncClient, x_api_key_header: dict[str, str]
) -> None:
    owner_id = str(uuid.uuid4())
    owner_password = "<PASSWORD>"
    owner_data = {"user_public_id": owner_id, "password_hash": owner_password}
    response = await async_client.post(
        f"{settings.API_V1_STR}/owner/",
        headers=x_api_key_header,
        json=owner_data,
        params={"owner_id": str(owner_id)},
    )
    assert response.status_code == 201

    response_2 = await async_client.post(
        f"{settings.API_V1_STR}/owner/",
        headers=x_api_key_header,
        json=owner_data,
        params={"owner_id": str(owner_id)},
    )

    assert response_2.status_code == 409
