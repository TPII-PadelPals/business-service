import uuid

from app.services.business_service import BusinessService
from app.services.padel_court_service import PadelCourtService
from app.utilities.dependencies import SessionDep


class CourtOwnerVerificationService:
    async def verification_of_court_owner(
        self,
        session: SessionDep,
        user_id: uuid.UUID,
        court_name: str,
        business_public_id: uuid.UUID,
    ) -> None:
        await BusinessService().validate_user_is_owner(
            session, business_public_id, user_id
        )
        await PadelCourtService().get_padel_court(
            session, court_name, business_public_id
        )
