import uuid

from app.services.business_service import BusinessService
from app.services.padel_court_service import PadelCourtService
from app.utilities.dependencies import SessionDep
from app.utilities.exceptions import (
    BusinessNotFoundException,
    BusinessNotFoundHTTPException,
)


class CourtOwnerVerificationService:
    async def verification_of_court_owner(
        self,
        session: SessionDep,
        user_id: uuid.UUID,
        court_name: str,
        business_public_id: uuid.UUID,
    ) -> None:
        try:
            await BusinessService().validate_user_is_owner(
                session, business_public_id, user_id
            )
        except BusinessNotFoundException as e:
            raise BusinessNotFoundHTTPException(str(e))
        except Exception as e:
            raise e
        await PadelCourtService().get_padel_court(
            session, court_name, business_public_id
        )

    async def verification_of_court_owner_without_name(
        self,
        session: SessionDep,
        user_id: uuid.UUID,
        business_public_id: uuid.UUID,
        court_public_id: uuid.UUID,
    ) -> None:
        try:
            await BusinessService().validate_user_is_owner(
                session, business_public_id, user_id
            )
        except BusinessNotFoundException as e:
            raise BusinessNotFoundHTTPException(str(e))
        except Exception as e:
            raise e
        await PadelCourtService().get_padel_court_without_name(
            session, court_public_id, business_public_id
        )
