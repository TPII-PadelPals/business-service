import uuid
from unittest.mock import patch

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.business import Business, BusinessesFilters, BusinessesPublic
from app.services.business_service import BusinessService


async def test_get_businesses_all(session: AsyncSession) -> None:
    coords = (0.1, 0.4)

    businesses = [
        Business(
            business_public_id=uuid.uuid4(),
            name="Service Test 1",
            location="Location 1",
            owner_id=uuid.uuid4(),
            latitude=coords[0],
            longitude=coords[1],
        ),
        Business(
            business_public_id=uuid.uuid4(),
            name="Service Test 2",
            location="Location 2",
            owner_id=uuid.uuid4(),
            latitude=coords[0],
            longitude=coords[1],
        ),
    ]

    mock_result = BusinessesPublic(data=businesses, count=len(businesses))

    with patch(
        "app.repository.business_repository.BusinessRepository.get_businesses"
    ) as mock_get:
        mock_get.return_value = mock_result

        service = BusinessService()
        result = await service.get_businesses(session)

        mock_get.assert_called_once_with(0, 100)
        assert result.count == 2
        assert len(result.data) == 2
        assert result.data[0].name == "Service Test 1"
        assert result.data[1].name == "Service Test 2"


async def test_get_businesses_with_owner_filter(session: AsyncSession) -> None:
    owner_id = uuid.uuid4()
    coords = (0.1, 0.4)

    businesses = [
        Business(
            business_public_id=uuid.uuid4(),
            name="Owner Business 1",
            location="Owner Location 1",
            owner_id=owner_id,
            latitude=coords[0],
            longitude=coords[1],
        ),
        Business(
            business_public_id=uuid.uuid4(),
            name="Owner Business 2",
            location="Owner Location 2",
            owner_id=owner_id,
            latitude=coords[0],
            longitude=coords[1],
        ),
    ]

    mock_result = BusinessesPublic(data=businesses, count=len(businesses))

    with patch(
        "app.repository.business_repository.BusinessRepository.get_businesses"
    ) as mock_get:
        mock_get.return_value = mock_result

        service = BusinessService()
        business_filter = BusinessesFilters(owner_id=owner_id)
        result = await service.get_businesses(session, business_filter=business_filter)

        mock_get.assert_called_once_with(0, 100, owner_id=owner_id)
        assert result.count == 2
        assert all(b.owner_id == owner_id for b in result.data)


async def test_get_businesses_with_pagination(session: AsyncSession) -> None:
    coords = (0.1, 0.4)

    businesses_page1 = [
        Business(
            business_public_id=uuid.uuid4(),
            name="Page1 Business 1",
            location="Location 1",
            owner_id=uuid.uuid4(),
            latitude=coords[0],
            longitude=coords[1],
        ),
        Business(
            business_public_id=uuid.uuid4(),
            name="Page1 Business 2",
            location="Location 2",
            owner_id=uuid.uuid4(),
            latitude=coords[0],
            longitude=coords[1],
        ),
    ]

    with patch(
        "app.repository.business_repository.BusinessRepository.get_businesses"
    ) as mock_get:
        mock_get.return_value = BusinessesPublic(data=businesses_page1, count=5)

        service = BusinessService()
        result = await service.get_businesses(session, skip=0, limit=2)

        mock_get.assert_called_once_with(0, 2)
        assert result.count == 5
        assert len(result.data) == 2
