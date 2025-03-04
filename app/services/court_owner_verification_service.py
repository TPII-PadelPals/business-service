import uuid

from app.services.business_service import BusinessService
from app.services.padel_court_service import PadelCourtService
from app.utilities.dependencies import SessionDep


class CourtOwnerVerificationService:
    async def _verification_of_business(
        self, session: SessionDep, user_id: uuid.UUID, business_id: uuid.UUID
    ) -> None:
        business_service = BusinessService()
        await business_service.validate_user_is_owned(session, business_id, user_id)

    async def _verification_of_court_business(
        self,
        session: SessionDep,
        court_name: str,
        business_id: uuid.UUID,
    ) -> None:
        padel_court_service = PadelCourtService()
        await padel_court_service.get_padel_court(session, court_name, business_id)

    async def verification_of_court_owner(
        self,
        session: SessionDep,
        user_id: uuid.UUID,
        court_name: str,
        business_id: uuid.UUID,
    ) -> None:
        await self._verification_of_business(session, user_id, business_id)
        await self._verification_of_court_business(session, court_name, business_id)
