import pytest

from app.models.business import BusinessCreate
from app.repository.business_repository import BusinessRepository


@pytest.mark.asyncio
async def test_create_business(db):
    repository = BusinessRepository(db)
    business_data = BusinessCreate(name="Padel Si", location="Av La plata 210")

    created_business = await repository.create_business(business_data)

    assert created_business.name == business_data.name
    assert created_business.location == business_data.location
