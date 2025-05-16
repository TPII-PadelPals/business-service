import uuid
from decimal import Decimal
from unittest.mock import patch

from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.padel_court import PadelCourt, PadelCourtFilter, PadelCourtsPublic
from app.services.padel_court_service import PadelCourtService


async def test_get_padel_courts_all(session: AsyncSession) -> None:
    courts = [
        PadelCourt(
            id=1,
            court_public_id=uuid.uuid4(),
            business_public_id=uuid.uuid4(),
            name="Service Court X",
            price_per_hour=Decimal("100.00"),
        ),
        PadelCourt(
            id=2,
            court_public_id=uuid.uuid4(),
            business_public_id=uuid.uuid4(),
            name="Service Court Y",
            price_per_hour=Decimal("150.00"),
        ),
    ]

    mock_result = PadelCourtsPublic(data=courts, count=len(courts))

    with patch(
        "app.repository.padel_court_repository.PadelCourtRepository.get_padel_courts"
    ) as mock_get:
        mock_get.return_value = mock_result

        service = PadelCourtService()
        result = await service.get_padel_courts(session)

        mock_get.assert_called_once_with(None, None, 0, 100)
        assert result.count == 2
        assert len(result.data) == 2
        assert result.data[0].name == "Service Court X"
        assert result.data[1].name == "Service Court Y"


async def test_get_padel_courts_with_business_filter(session: AsyncSession) -> None:
    business_public_id = uuid.uuid4()

    courts = [
        PadelCourt(
            id=1,
            court_public_id=uuid.uuid4(),
            business_public_id=business_public_id,
            name="Business Court A",
            price_per_hour=Decimal("100.00"),
        ),
        PadelCourt(
            id=2,
            court_public_id=uuid.uuid4(),
            business_public_id=business_public_id,
            name="Business Court B",
            price_per_hour=Decimal("150.00"),
        ),
    ]

    mock_result = PadelCourtsPublic(data=courts, count=len(courts))

    with patch(
        "app.repository.padel_court_repository.PadelCourtRepository.get_padel_courts"
    ) as mock_get:
        mock_get.return_value = mock_result

        service = PadelCourtService()
        prov_court_filters = PadelCourtFilter(business_public_id=business_public_id)
        result = await service.get_padel_courts(
            session, prov_court_filters=prov_court_filters
        )

        mock_get.assert_called_once_with(business_public_id, None, 0, 100)
        assert result.count == 2
        assert all(c.business_public_id == business_public_id for c in result.data)


async def test_get_padel_courts_with_pagination(session: AsyncSession) -> None:
    courts_page1 = [
        PadelCourt(
            id=1,
            court_public_id=uuid.uuid4(),
            business_public_id=uuid.uuid4(),
            name="Page1 Court 1",
            price_per_hour=Decimal("100.00"),
        ),
        PadelCourt(
            id=2,
            court_public_id=uuid.uuid4(),
            business_public_id=uuid.uuid4(),
            name="Page1 Court 2",
            price_per_hour=Decimal("150.00"),
        ),
    ]

    with patch(
        "app.repository.padel_court_repository.PadelCourtRepository.get_padel_courts"
    ) as mock_get:
        mock_get.return_value = PadelCourtsPublic(data=courts_page1, count=5)

        service = PadelCourtService()
        result = await service.get_padel_courts(session, skip=0, limit=2)

        mock_get.assert_called_once_with(None, None, 0, 2)
        assert result.count == 5
        assert len(result.data) == 2


async def test_get_padel_courts_with_business_and_user_filter(
    session: AsyncSession,
) -> None:
    business_public_id = uuid.uuid4()
    user_id = uuid.uuid4()

    courts = [
        PadelCourt(
            id=1,
            court_public_id=uuid.uuid4(),
            business_public_id=business_public_id,
            name="Owner Court A",
            price_per_hour=Decimal("100.00"),
        ),
        PadelCourt(
            id=2,
            court_public_id=uuid.uuid4(),
            business_public_id=business_public_id,
            name="Owner Court B",
            price_per_hour=Decimal("150.00"),
        ),
    ]

    mock_result = PadelCourtsPublic(data=courts, count=len(courts))

    with patch(
        "app.repository.padel_court_repository.PadelCourtRepository.get_padel_courts"
    ) as mock_get:
        mock_get.return_value = mock_result

        service = PadelCourtService()
        prov_court_filters = PadelCourtFilter(business_public_id=business_public_id)
        result = await service.get_padel_courts(
            session, prov_court_filters=prov_court_filters, user_id=user_id
        )

        mock_get.assert_called_once_with(business_public_id, user_id, 0, 100)
        assert result.count == 2
        assert all(c.business_public_id == business_public_id for c in result.data)
