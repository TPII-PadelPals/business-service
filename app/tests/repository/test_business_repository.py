import uuid

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.business import BusinessCreate
from app.repository.business_repository import BusinessRepository


async def test_create_business(session: AsyncSession):
    repository = BusinessRepository(session)
    business_data = BusinessCreate(name="Padel Si", location="Av La plata 210")
    owner_id = uuid.uuid4()

    longitude = 0.1
    latitude = 0.4
    created_business = await repository.create_business(
        owner_id, business_data, longitude, latitude
    )

    assert created_business.name == business_data.name
    assert created_business.location == business_data.location
    assert created_business.owner_id == owner_id
    assert created_business.longitude == longitude
    assert created_business.latitude == latitude


async def test_get_business(session: AsyncSession) -> None:
    repository = BusinessRepository(session)
    business_data = BusinessCreate(name="Padel Si", location="Av La plata 210")
    owner_id = uuid.uuid4()
    longitude = 0.1
    latitude = 0.4
    new_business = await repository.create_business(owner_id, business_data, longitude, latitude)
    # test
    business = await repository.get_business(new_business.id)

    assert business.name == business_data.name
    assert business.location == business_data.location
    assert business.owner_id == owner_id


async def test_get_all_businesses(session: AsyncSession) -> None:
    repository = BusinessRepository(session)
    owner1_id = uuid.uuid4()
    owner2_id = uuid.uuid4()
    coords = (0.1, 0.4)

    business1 = BusinessCreate(name="Business One", location="Location One")
    business2 = BusinessCreate(name="Business Two", location="Location Two")
    business3 = BusinessCreate(name="Business Three", location="Location Three")

    await repository.create_business(owner1_id, business1, *coords)
    await repository.create_business(owner2_id, business2, *coords)
    await repository.create_business(owner1_id, business3, *coords)

    result = await repository.get_businesses()

    assert result.count >= 3
    assert len(result.data) >= 3
    business_names = [b.name for b in result.data]
    assert "Business One" in business_names
    assert "Business Two" in business_names
    assert "Business Three" in business_names


async def test_get_businesses_filtered_by_owner(session: AsyncSession) -> None:
    repository = BusinessRepository(session)
    owner1_id = uuid.uuid4()
    owner2_id = uuid.uuid4()
    coords = (0.1, 0.4)

    business1 = BusinessCreate(name="Owner1 Business A", location="Location A")
    business2 = BusinessCreate(name="Owner2 Business", location="Location B")
    business3 = BusinessCreate(name="Owner1 Business B", location="Location C")

    await repository.create_business(owner1_id, business1, *coords)
    await repository.create_business(owner2_id, business2, *coords)
    await repository.create_business(owner1_id, business3, *coords)

    result = await repository.get_businesses(owner_id=owner1_id)

    assert result.count == 2
    assert len(result.data) == 2
    business_names = [b.name for b in result.data]
    assert "Owner1 Business A" in business_names
    assert "Owner1 Business B" in business_names
    assert "Owner2 Business" not in business_names


async def test_get_businesses_with_pagination(session: AsyncSession) -> None:
    repository = BusinessRepository(session)
    owner_id = uuid.uuid4()
    coords = (0.1, 0.4)

    for i in range(1, 6):
        business = BusinessCreate(
            name=f"Paginated Business {i}", location=f"Location {i}"
        )
        await repository.create_business(owner_id, business, *coords)

    page1 = await repository.get_businesses(skip=0, limit=2)

    page2 = await repository.get_businesses(skip=2, limit=2)

    assert page1.count >= 5
    assert len(page1.data) == 2

    assert page2.count >= 5
    assert len(page2.data) == 2

    page1_names = [b.name for b in page1.data]
    page2_names = [b.name for b in page2.data]
    assert not any(name in page1_names for name in page2_names)
