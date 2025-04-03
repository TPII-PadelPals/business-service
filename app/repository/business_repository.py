import uuid

from sqlalchemy import func
from sqlmodel import select

from app.models.business import Business, BusinessCreate, BusinessesPublic
from app.utilities.exceptions import BusinessNotFoundException


class BusinessRepository:
    def __init__(self, session) -> None:
        self.session = session

    async def create_business(
        self,
        owner_id: uuid.UUID,
        business_in: BusinessCreate,
        longitude: float,
        latitude: float,
    ) -> Business:
        new_business = Business.model_validate(
            business_in,
            update={"owner_id": owner_id, "longitude": longitude, "latitude": latitude},
        )
        self.session.add(new_business)
        await self.session.commit()
        await self.session.refresh(new_business)
        return new_business

    async def get_business(self, id: uuid.UUID) -> Business:
        query = select(Business).where(Business.id == id)
        result = await self.session.exec(query)
        business = result.first()
        if not business:
            raise BusinessNotFoundException()
        return business

    async def get_businesses(
        self, owner_id: uuid.UUID = None, skip: int = 0, limit: int = 100
    ) -> BusinessesPublic:
        query = select(Business)
        if owner_id is not None:
            query = query.where(Business.owner_id == owner_id)

        count_query = select(func.count()).select_from(query.subquery())
        count_result = await self.session.exec(count_query)
        total_count = count_result.one()

        query = query.offset(skip).limit(limit)
        result = await self.session.exec(query)
        businesses = result.all()

        return BusinessesPublic(data=businesses, count=total_count)
