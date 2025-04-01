import uuid

from sqlalchemy import func
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.business import Business
from app.models.padel_court import PadelCourt, PadelCourtCreate, PadelCourtsPublic
from app.utilities.exceptions import (
    BusinessNotFoundException,
    NotFoundException,
    UnauthorizedPadelCourtOperationException,
)


class PadelCourtRepository:
    def __init__(self, session: AsyncSession) -> None:
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
            padel_court_in, update={"business_public_id": business_id}
        )
        self.session.add(new_padel_court)
        await self.session.commit()
        await self.session.refresh(new_padel_court)
        return new_padel_court

    async def get_padel_court(
        self, court_name: str, business_id: uuid.UUID
    ) -> PadelCourt:
        query = select(PadelCourt).where(
            and_(
                PadelCourt.name == court_name,
                PadelCourt.business_public_id == business_id,
            )
        )
        result = await self.session.exec(query)
        padel_court = result.first()
        if not padel_court:
            raise NotFoundException("padel court")
        return padel_court

    async def get_padel_courts(
        self, business_id: uuid.UUID = None, user_id: uuid.UUID = None, skip: int = 0, limit: int = 100
    ) -> PadelCourtsPublic:
        
        query = select(PadelCourt)

        if business_id and user_id:
             query = query.join(Business, PadelCourt.business_public_id == Business.id).where(
                and_(
                    PadelCourt.business_public_id == business_id,
                    Business.owner_id == user_id
                )
            )
        
        count_query = select(func.count()).select_from(query.subquery())
        count_result = await self.session.exec(count_query)
        total_count = count_result.one()

        query = query.offset(skip).limit(limit)
        result = await self.session.exec(query)
        padel_courts = result.all()

        return PadelCourtsPublic(data=padel_courts, count=total_count)
