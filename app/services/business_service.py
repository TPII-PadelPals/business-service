import uuid

from app.models.business import Business, BusinessesPublic
from app.models.padel_court import PadelCourtsPublic
from app.repository.business_repository import BusinessRepository
from app.repository.padel_court_repository import PadelCourtRepository
from app.utilities.dependencies import SessionDep
from app.utilities.exceptions import UnauthorizedUserException


class BusinessService:
    async def get_business(
        self, session: SessionDep, business_id: uuid.UUID
    ) -> Business:
        repo = BusinessRepository(session)
        return await repo.get_business(business_id)

    async def validate_user_is_owner(
        self, session: SessionDep, business_id: uuid.UUID, user_id: uuid.UUID
    ):
        business = await self.get_business(session, business_id)
        if not business.is_owned(user_id):
            raise UnauthorizedUserException()

    async def get_businesses(
        self, session: SessionDep, owner_id: uuid.UUID = None, skip: int = 0, limit: int = 100
    ) -> BusinessesPublic:
        repo = BusinessRepository(session)
        return await repo.get_businesses(owner_id, skip, limit)