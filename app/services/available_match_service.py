import datetime
import uuid

from sqlalchemy.exc import IntegrityError

from app.models.available_date import AvailableMatch, AvailableMatchCreate
from app.repository.available_date_repository import AvailableDateRepository
from app.services.court_owner_verification_service import (
    CourtOwnerVerificationService,
)
from app.utilities.dependencies import SessionDep
from app.utilities.exceptions import NotUniqueException


class AvailableDateService:
    async def create_available_date(
        self,
        session: SessionDep,
        user_id: uuid.UUID,
        court_name: str,
        business_id: uuid.UUID,
        available_date_in: AvailableMatchCreate,
    ) -> list[AvailableMatch]:
        service_aux = CourtOwnerVerificationService()
        await service_aux.verification_of_court_owner(
            session, user_id, court_name, business_id
        )

        available_date_in.validate_create()
        repo = AvailableDateRepository(session)
        try:
            result = await repo.create_available_dates(available_date_in)
            return result
        except IntegrityError:
            await session.rollback()
            raise NotUniqueException("available date")
        except Exception as e:
            raise e

    async def get_available_date(
        self,
        session: SessionDep,
        court_name: str,
        business_id: uuid.UUID,
        date: datetime.date,
    ) -> list[AvailableMatch]:
        repo = AvailableDateRepository(session)
        available_dates = await repo.get_available_dates(court_name, business_id, date)
        return available_dates

    async def update_for_reserve_available_date(
        self,
        session: SessionDep,
        court_name: str,
        business_id: uuid.UUID,
        date: datetime.date,
        hour: int,
    ) -> AvailableMatch:
        repo = AvailableDateRepository(session)
        available_date = await repo.reserve_available_time(
            court_name, business_id, date, hour
        )
        return available_date

    async def delete_available_date(
        self,
        session: SessionDep,
        user_id: uuid.UUID,
        court_name: str,
        business_id: uuid.UUID,
        date: datetime.date,
    ) -> None:
        service_aux = CourtOwnerVerificationService()
        await service_aux.verification_of_court_owner(
            session, user_id, court_name, business_id
        )

        repo = AvailableDateRepository(session)
        await repo.delete_available_date(court_name, business_id, date)
        return
