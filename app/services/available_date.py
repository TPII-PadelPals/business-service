import uuid

from sqlalchemy.exc import IntegrityError

from app.models.available_date import AvailableDateCreate, AvailableDate
from app.repository.available_date_repository import AvailableDateRepository
from app.services.verification_of_court_owner_service import VerificationOfCourtOwnerService
from app.utilities.dependencies import SessionDep
from app.utilities.exceptions import NotUniqueException


class AvailableDateService:
    async def create_available_date(
            self,
            session: SessionDep,
            user_id: uuid.UUID,
            court_name: str,
            business_id: uuid.UUID,
            available_date_in: AvailableDateCreate
    ) -> list[AvailableDate]:
        service_aux = VerificationOfCourtOwnerService()
        await service_aux.verification_of_court_owner(session, user_id, court_name, business_id)

        available_date_in.validate_create()
        repo = AvailableDateRepository(session)
        try:
            result = await repo.create_available_dates(available_date_in)
            return result
        except IntegrityError:
            session.rollback()
            raise NotUniqueException("available date")
        except Exception as e:
            raise e
