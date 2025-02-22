import uuid
from decimal import Decimal

import pytest

from app.models.business import BusinessCreate
from app.models.padel_court import PadelCourtCreate, PadelCourt
from app.repository.business_repository import BusinessRepository
from app.services.verification_of_court_owner_service import VerificationOfCourtOwnerService
from sqlmodel.ext.asyncio.session import AsyncSession

from app.utilities.exceptions import BusinessNotFoundException, UnauthorizedUserException, NotFoundException


async def test_verification_of_court_owner_service(session: AsyncSession) -> None:
    business_repository = BusinessRepository(session)
    business_data = {
        "name":"Padel Ya",
        "location": "Av La plata 210"
    }
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()
    padel_court_data = {
        "name": str("Padel Si"),
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
    service = VerificationOfCourtOwnerService()
    # assert
    await service.verification_of_court_owner(
        session,
        owner_id,
        str(padel_court_data["name"]),
        business_id
    )


async def test_verification_fail_not_business_of_court_owner_service(session: AsyncSession) -> None:
    service = VerificationOfCourtOwnerService()
    # test
    with pytest.raises(BusinessNotFoundException) as e:
        await service.verification_of_court_owner(
            session,
            uuid.uuid4(),
            "NAME",
            uuid.uuid4()
        )
    # assert
    assert str(e.value) == "Business not found"


async def test_verification_fail_not_owner_of_court_owner_service(session: AsyncSession) -> None:
    business_data = {
        "name":"Padel Ya",
        "location": "Av La plata 210"
    }
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()

    business_repository = BusinessRepository(session)
    created_business = await business_repository.create_business(owner_id, business)
    business_id = created_business.id

    not_owner = uuid.uuid4()
    limit = 100
    while not_owner == created_business.id:
        not_owner = uuid.uuid4()
        limit -= 1
        if limit == 0:
            assert False

    service = VerificationOfCourtOwnerService()
    # test
    with pytest.raises(UnauthorizedUserException) as e:
        await service.verification_of_court_owner(
            session,
            not_owner,
            "NAME",
            business_id
        )
    # assert
    assert e.value.detail == "User is not the owner"



async def test_verification_fail_not_court_of_court_owner_service(session: AsyncSession) -> None:
    business_data = {
        "name":"Padel Ya",
        "location": "Av La plata 210"
    }
    business = BusinessCreate(**business_data)
    owner_id = uuid.uuid4()

    business_repository = BusinessRepository(session)
    created_business = await business_repository.create_business(owner_id, business)
    business_id = created_business.id


    service = VerificationOfCourtOwnerService()
    # test
    with pytest.raises(NotFoundException) as e:
        await service.verification_of_court_owner(
            session,
            owner_id,
            "NAME",
            business_id
        )
    # assert
    assert e.value.detail == "Padel court not found"