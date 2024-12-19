import uuid

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.business import BusinessCreate
from app.repository.business_repository import BusinessRepository


async def test_create_business(session: AsyncSession):
    repository = BusinessRepository(session)
    business_data = BusinessCreate(name="Padel Si", location="Av La plata 210")
    owner_id = uuid.uuid4()

    created_business = await repository.create_business(owner_id, business_data)

    assert created_business.name == business_data.name
    assert created_business.location == business_data.location
    assert created_business.owner_id == owner_id
