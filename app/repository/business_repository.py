import uuid

from app.models.business import Business, BusinessCreate
from app.utilities.exceptions import BusinessNotFoundException
from sqlmodel import select

class BusinessRepository:
    def __init__(self, session):
        self.session = session


    async def create_business(
        self, owner_id: uuid.UUID, business_in: BusinessCreate
    ) -> Business:
        new_business = Business.model_validate(
            business_in, update={"owner_id": owner_id}
        )
        self.session.add(new_business)
        await self.session.commit()
        await self.session.refresh(new_business)
        return new_business


    async def get_business(self, owner_id: uuid.UUID) -> Business:
        query = select(Business).where(Business.owner_id == owner_id)
        result = await self.session.exec(query)
        business = result.first()
        if not business:
            raise BusinessNotFoundException()
        return business
