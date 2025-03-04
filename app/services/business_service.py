import uuid

from app.models.business import Business
from app.repository.business_repository import BusinessRepository
from app.utilities.dependencies import SessionDep


class BusinessService:
    async def get_business(
        self, session: SessionDep, business_id: uuid.UUID
    ) -> Business:
        repo = BusinessRepository(session)
        return await repo.get_business(business_id)
