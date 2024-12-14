import uuid

from fastapi.testclient import TestClient

from app.core.config import settings


async def _create_business(
    client, x_api_key, name: str, location: str, parameters: dict[str, int]
):
    business_data = {"name": name, "location": location}
    response = await client.post(
        f"{settings.API_V1_STR}/businesses/",
        headers=x_api_key,
        json=business_data,
        params=parameters,
    )
    return response.json()


async def test_create_padel_court_with_existing_business(
    async_client: TestClient, x_api_key_header: dict[str, str]
) -> None:
    owner_id = uuid.uuid4()

    new_business = await _create_business(
        client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": owner_id},
    )

    padel_court_data = {"name": "Cancha 1", "price_per_hour": "15000.00"}

    response = await async_client.post(
        f"{settings.API_V1_STR}/padel-courts/",
        headers=x_api_key_header,
        json=padel_court_data,
        params={"business_id": new_business["id"], "owner_id": owner_id},
    )

    assert response.status_code == 201
    content = response.json()

    assert content["name"] == padel_court_data["name"]
    assert content["price_per_hour"] == padel_court_data["price_per_hour"]
    assert "id" in content
    assert "business_id" in content


async def test_create_padel_court_with_nonexisting_business_id_returns_error(
    async_client: TestClient, x_api_key_header: dict[str, str]
) -> None:
    owner_id = uuid.uuid4()
    nonexisting_business_id = uuid.uuid4()

    _new_business = await _create_business(
        client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": owner_id},
    )

    padel_court_data = {"name": "Cancha 1", "price_per_hour": "1500000"}

    response = await async_client.post(
        f"{settings.API_V1_STR}/padel-courts/",
        headers=x_api_key_header,
        json=padel_court_data,
        params={"business_id": nonexisting_business_id, "owner_id": owner_id},
    )

    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Business not found"


async def test_create_padel_court_with_unauthorized_owner_id_returns_error(
    async_client: TestClient, x_api_key_header: dict[str, str]
) -> None:
    owner_id = uuid.uuid4()

    new_business = await _create_business(
        client=async_client,
        x_api_key=x_api_key_header,
        name="Paloma SA",
        location="Polaca 530",
        parameters={"owner_id": owner_id},
    )

    unauthorized_owner_id = uuid.uuid4()

    padel_court_data = {"name": "Cancha 20", "price_per_hour": "30000"}

    response = await async_client.post(
        f"{settings.API_V1_STR}/padel-courts/",
        headers=x_api_key_header,
        json=padel_court_data,
        params={"business_id": new_business["id"], "owner_id": unauthorized_owner_id},
    )

    assert response.status_code == 403
    content = response.json()
    assert content["detail"] == "Not enough permissions"
