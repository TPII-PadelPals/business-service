import uuid
from datetime import date

from sqlmodel.ext.asyncio.session import AsyncSession

from decimal import Decimal
from app.models.available_date import AvailableDateCreate
from app.models.business import BusinessCreate
from app.models.padel_court import PadelCourtCreate, PadelCourt
from app.repository.available_date_repository import AvailableDateRepository
from app.repository.business_repository import BusinessRepository


async def test_create_available_dates(session: AsyncSession) -> None:
    business_repository = BusinessRepository(session)
    business_data = {
        "name":"Padel Ya",
        "location": "Av La plata 210"
    }
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()
    padel_court_data = {
        "name":"Padel Si",
        "price_per_hour":Decimal("15000.00")
    }
    padel_court_in = PadelCourtCreate(**padel_court_data)
    created_business = await business_repository.create_business(owner_id, business)
    business_id = created_business.id
    new_padel_court = PadelCourt.model_validate(
        padel_court_in, update={"business_id": business_id}
    )
    session.add(new_padel_court)
    await session.commit()
    await session.refresh(new_padel_court)

    available_date_create_data = {
        "court_name": padel_court_data["name"],
        "business_id": business_id,
        "date": date(2025, 1, 1),
        "initial_hour": 5,
        "number_of_games": 5
    }

    repository_available_date = AvailableDateRepository(session)
    create = AvailableDateCreate(**available_date_create_data)
    # test
    dates = await repository_available_date.create_available_dates(create)
    # assert
    assert len(dates) == 5
