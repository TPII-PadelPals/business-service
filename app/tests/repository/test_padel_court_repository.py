from decimal import Decimal

from app.models.business import BusinessCreate
from app.models.padel_court import PadelCourtCreate
from app.repository.business_repository import BusinessRepository
from app.repository.padel_court_repository import PadelCourtRepository


async def test_create_padel_court(db):
    repository = BusinessRepository(db)
    business_data = BusinessCreate(name="Padel Ya", location="Av La plata 210")

    created_business = await repository.create_business(business_data)

    repository = PadelCourtRepository(db)
    padel_court = PadelCourtCreate(name="Padel Si", price_per_hour=Decimal("15000.00"))

    created_padel_court = await repository.create_padel_court(
        created_business.id, padel_court
    )

    assert created_padel_court.name == padel_court.name
    assert created_padel_court.price_per_hour == padel_court.price_per_hour
