import uuid

from sqlmodel import select, and_
from app.models.business import Business
from app.models.padel_court import PadelCourt, PadelCourtCreate
from app.utilities.exceptions import (
    BusinessNotFoundException,
    UnauthorizedPadelCourtOperationException, NotFoundException,
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


    async def get_padel_court(self, court_name: str, business_id: uuid.UUID) -> PadelCourt:
        query = select(PadelCourt).where(and_(PadelCourt.name == court_name, PadelCourt.business_id == business_id))
        result = await self.session.exec(query)
        padel_court = result.first()
        if not padel_court:
            raise NotFoundException("padel court")
        return padel_court
        # raise NotFoundException("padel court")