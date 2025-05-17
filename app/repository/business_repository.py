import uuid
from typing import Any

from sqlalchemy import func
from sqlmodel import select

from app.models.business import (
    Business,
    BusinessCreate,
    BusinessesPublic,
    BusinessUpdate,
)
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
        query = select(Business).where(Business.business_public_id == id)
        result = await self.session.exec(query)
        business = result.first()
        if not business:
            raise BusinessNotFoundException()
        return business

    async def get_businesses(
        self,
        skip: int = 0,
        limit: int = 100,
        **filters: Any,
    ) -> BusinessesPublic:
        query = select(Business)
        # Filters
        for key, value in filters.items():
            attr = getattr(Business, key)
            query = query.where(attr == value)
        count_query = select(func.count()).select_from(query.subquery())
        count_result = await self.session.exec(count_query)
        total_count = count_result.one()

        query = query.offset(skip).limit(limit)
        result = await self.session.exec(query)
        businesses = result.all()

        return BusinessesPublic(data=businesses, count=total_count)

    async def update_business(
        self, business_public_id: uuid.UUID, business_in: BusinessUpdate
    ) -> Business:
        business = await self.get_business(business_public_id)
        update_dict = business_in.model_dump(exclude_none=True)
        business.sqlmodel_update(update_dict)
        self.session.add(business)
        await self.session.commit()
        await self.session.refresh(business)
        return business
