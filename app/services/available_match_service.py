import datetime
import uuid

from sqlalchemy.exc import IntegrityError

from app.models.available_match import AvailableMatch, AvailableMatchCreate
from app.repository.available_matches_repository import AvailableMatchesRepository
from app.services.court_owner_verification_service import (
    CourtOwnerVerificationService,
)
from app.utilities.dependencies import SessionDep
from app.utilities.exceptions import CourtAlreadyReservedException, NotUniqueException


class AvailableMatchService:
    async def create_available_matches_in_date(
        self,
        session: SessionDep,
        user_id: uuid.UUID,
        court_name: str,
        business_public_id: uuid.UUID,
        available_matches_in: AvailableMatchCreate,
    ) -> list[AvailableMatch]:
        service_aux = CourtOwnerVerificationService()
        await service_aux.verification_of_court_owner(
            session, user_id, court_name, business_public_id
        )

        available_matches_in.validate_create()
        repo = AvailableMatchesRepository(session)
        try:
            result = await repo.create_available_matches_in_date(available_matches_in)
            return result
        except IntegrityError:
            await session.rollback()
            raise NotUniqueException("available date")
        except Exception as e:
            raise e

    async def get_available_matches_in_date(
        self,
        session: SessionDep,
        court_name: str,
        business_public_id: uuid.UUID,
        date: datetime.date,
    ) -> list[AvailableMatch]:
        repo = AvailableMatchesRepository(session)
        available_matches = await repo.get_available_matches_in_date(
            court_name, business_public_id, date
        )
        return available_matches

    async def reserve_available_match(
        self,
        session: SessionDep,
        court_name: str,
        business_public_id: uuid.UUID,
        date: datetime.date,
        hour: int,
    ) -> AvailableMatch:
        repo = AvailableMatchesRepository(session)
        available_match = await repo.get_available_match(
            court_name, business_public_id, date, hour
        )
        if available_match.is_reserved():
            raise CourtAlreadyReservedException(court_name)
        available_match.set_reserve()
        return await repo.update_available_match(available_match)

    async def delete_available_matches_in_date(
        self,
        session: SessionDep,
        user_id: uuid.UUID,
        court_name: str,
        business_public_id: uuid.UUID,
        date: datetime.date,
    ) -> None:
        service_aux = CourtOwnerVerificationService()
        await service_aux.verification_of_court_owner(
            session, user_id, court_name, business_public_id
        )

        repo = AvailableMatchesRepository(session)
        await repo.delete_available_matches_in_date(court_name, business_public_id, date)
        return
