import uuid
from typing import Any

from sqlalchemy import func
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.business import Business
from app.models.padel_court import (
    PadelCourt,
    PadelCourtCreate,
    PadelCourtsPublic,
    PadelCourtUpdate,
)
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
        business_public_id: uuid.UUID,
        padel_court_in: PadelCourtCreate,
    ) -> PadelCourt:
        query = select(Business).where(
            Business.business_public_id == business_public_id
        )
        result = await self.session.exec(query)
        business = result.first()
        if not business:
            raise BusinessNotFoundException()
        if owner_id != business.owner_id:
            raise UnauthorizedPadelCourtOperationException()
        new_padel_court = PadelCourt.model_validate(
            padel_court_in, update={"business_public_id": business_public_id}
        )
        self.session.add(new_padel_court)
        await self.session.commit()
        await self.session.refresh(new_padel_court)
        return new_padel_court

    async def get_padel_court(
        self, court_name: str, business_public_id: uuid.UUID
    ) -> PadelCourt:
        query = select(PadelCourt).where(
            and_(
                PadelCourt.name == court_name,
                PadelCourt.business_public_id == business_public_id,
            )
        )
        result = await self.session.exec(query)
        padel_court = result.first()
        if not padel_court:
            raise NotFoundException("padel court")
        return padel_court

    async def get_padel_court_without_name(
        self, court_public_id: uuid.UUID
    ) -> PadelCourt:
        query = select(PadelCourt).where(
            PadelCourt.court_public_id == court_public_id,
        )
        result = await self.session.exec(query)
        court = result.first()
        if not court:
            raise NotFoundException("padel court")
        return court

    async def get_padel_courts(
        self,
        business_public_id: uuid.UUID = None,
        user_id: uuid.UUID = None,
        skip: int = 0,
        limit: int = 100,
        **filters: Any,
    ) -> PadelCourtsPublic:
        query = select(PadelCourt)

        print("ASDASDASDASDASDASDASD")
        print(filters)
        print(business_public_id)
        if business_public_id and user_id:
            query = query.join(
                Business, PadelCourt.business_public_id == Business.business_public_id
            ).where(
                and_(
                    PadelCourt.business_public_id == business_public_id,
                    Business.owner_id == user_id,
                )
            )
        for key, value in filters.items():
            attr = getattr(PadelCourt, key)
            query = query.where(attr == value)

        count_query = select(func.count()).select_from(query.subquery())
        count_result = await self.session.exec(count_query)
        total_count = count_result.one()

        query = query.offset(skip).limit(limit)
        result = await self.session.exec(query)
        padel_courts = result.all()

        return PadelCourtsPublic(data=padel_courts, count=total_count)

    async def update_padel_court(
        self, court_public_id: uuid.UUID, court_in: PadelCourtUpdate
    ) -> PadelCourt:
        court = await self.get_padel_court_without_name(court_public_id)

        update_dict = court_in.model_dump(exclude_none=True)
        court.sqlmodel_update(update_dict)
        self.session.add(court)
        await self.session.commit()
        await self.session.refresh(court)
        return court
