import uuid

from app.models.business import Business
from app.repository.business_repository import BusinessRepository
from app.utilities.dependencies import SessionDep
from app.utilities.exceptions import UnauthorizedUserException


class BusinessService:
    async def get_business(
        self, session: SessionDep, business_id: uuid.UUID
    ) -> Business:
        repo = BusinessRepository(session)
        return await repo.get_business(business_id)

    async def validate_user_is_owned(self, session: SessionDep, business_id: uuid.UUID, user_id: uuid.UUID):
        business = await self.get_business(session, business_id)
        if not business.is_owned(user_id):
            raise UnauthorizedUserException()
