import uuid

from app.models.business import Business
from app.models.padel_court import PadelCourt, PadelCourtCreate
from app.utilities.exceptions import (
    BusinessNotFoundException,
    UnauthorizedPadelCourtOperationException,
)


class PadelCourtRepository:
    def __init__(self, session):
        self.session = session

    async def create_padel_court(
        self,
        owner_id: uuid.UUID,
        business_id: uuid.UUID,
        padel_court_in: PadelCourtCreate,
    ) -> PadelCourt:
        business = await self.session.get(Business, business_id)
        if not business:
            raise BusinessNotFoundException()
        if owner_id != business.owner_id:
            raise UnauthorizedPadelCourtOperationException()
        new_padel_court = PadelCourt.model_validate(
            padel_court_in, update={"business_id": business_id}
        )
        self.session.add(new_padel_court)
        await self.session.commit()
        await self.session.refresh(new_padel_court)
        return new_padel_court
