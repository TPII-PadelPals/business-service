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