import uuid
from decimal import Decimal

import pytest
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.business import BusinessCreate
from app.models.padel_court import PadelCourt, PadelCourtCreate
from app.repository.business_repository import BusinessRepository
from app.services.court_owner_verification_service import (
    CourtOwnerVerificationService,
)
from app.utilities.exceptions import (
    BusinessNotFoundException,
    NotFoundException,
    UnauthorizedUserException, BusinessNotFoundHTTPException,
)


async def test_verification_of_court_owner_service(session: AsyncSession) -> None:
    business_repository = BusinessRepository(session)
    business_data = {"name": "Padel Ya", "location": "Av La plata 210"}
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()
    padel_court_data = {"name": "Padel Si", "price_per_hour": Decimal("15000.00")}
    padel_court_in = PadelCourtCreate(**padel_court_data)
    longitude = 0.1
    latitude = 0.4
    created_business = await business_repository.create_business(
        owner_id, business, longitude, latitude
    )
    business_public_id = created_business.business_public_id
    new_padel_court = PadelCourt.model_validate(
        padel_court_in, update={"business_public_id": business_public_id}
    )
    session.add(new_padel_court)
    await session.commit()
    await session.refresh(new_padel_court)
    service = CourtOwnerVerificationService()
    # assert
    await service.verification_of_court_owner(
        session, owner_id, str(padel_court_data["name"]), business_public_id
    )


async def test_verification_fail_not_business_of_court_owner_service(
    session: AsyncSession,
) -> None:
    service = CourtOwnerVerificationService()
    # test
    with pytest.raises(BusinessNotFoundHTTPException) as e:
        await service.verification_of_court_owner(
            session, uuid.uuid4(), "NAME", uuid.uuid4()
        )
    # assert
    assert str(e.value.detail) == "Business not found"


async def test_verification_fail_not_owner_of_court_owner_service(
    session: AsyncSession,
) -> None:
    business_data = {"name": "Padel Ya", "location": "Av La plata 210"}
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()

    business_repository = BusinessRepository(session)
    longitude = 0.1
    latitude = 0.4
    created_business = await business_repository.create_business(
        owner_id, business, longitude, latitude
    )
    business_public_id = created_business.business_public_id

    not_owner = uuid.uuid4()
    limit = 100
    while not_owner == created_business.business_public_id:
        not_owner = uuid.uuid4()
        limit -= 1
        assert limit != 0

    service = CourtOwnerVerificationService()
    # test
    with pytest.raises(UnauthorizedUserException) as e:
        await service.verification_of_court_owner(
            session, not_owner, "NAME", business_public_id
        )
    # assert
    assert e.value.detail == "User is not the owner"


async def test_verification_fail_not_court_of_court_owner_service(
    session: AsyncSession,
) -> None:
    business_data = {"name": "Padel Ya", "location": "Av La plata 210"}
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()

    business_repository = BusinessRepository(session)
    longitude = 0.1
    latitude = 0.4
    created_business = await business_repository.create_business(
        owner_id, business, longitude, latitude
    )
    business_public_id = created_business.business_public_id

    service = CourtOwnerVerificationService()
    # test
    with pytest.raises(NotFoundException) as e:
        await service.verification_of_court_owner(
            session, owner_id, "NAME", business_public_id
        )
    # assert
    assert e.value.detail == "Padel court not found"
