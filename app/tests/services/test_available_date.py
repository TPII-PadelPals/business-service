import uuid
from decimal import Decimal
from datetime import date

from app.models.available_date import AvailableDateCreate
from app.models.business import BusinessCreate
from app.models.padel_court import PadelCourtCreate, PadelCourt
from app.repository.business_repository import BusinessRepository
from app.services.available_date import AvailableDateService
from sqlmodel.ext.asyncio.session import AsyncSession


async def create_available_dates(session: AsyncSession) -> None:
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

    business_repository = BusinessRepository(session)
    created_business = await business_repository.create_business(owner_id, business)
    business_id = created_business.id
    new_padel_court = PadelCourt.model_validate(
        padel_court_in, update={"business_id": business_id}
    )
    session.add(new_padel_court)
    await session.commit()
    await session.refresh(new_padel_court)

    service = AvailableDateService()
    data_available_date = {
        "court_name": str("35"),
        "business_id": uuid.uuid4(),
        "date": date(2025, 1, 1),
        "initial_hour": 5,
        "number_of_games":5,
    }
    available_date_create = AvailableDateCreate(**data_available_date)
    # test
    available_dates = await service.create_available_date(
        session,
        owner_id,
        str(padel_court_data["name"]),
        business_id,
        available_date_create
    )
    # assert
    assert len(available_dates) == 5