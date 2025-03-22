import uuid

from sqlmodel import select

from app.models.business import Business, BusinessCreate
from app.utilities.exceptions import BusinessNotFoundException


class BusinessRepository:
    def __init__(self, session) -> None:
        self.session = session

    async def create_business(
        self, owner_id: uuid.UUID, business_in: BusinessCreate, longitude: float | None = None, latitude: float | None = None
    ) -> Business:
        new_business = Business.model_validate(
            business_in, update={"owner_id": owner_id, "longitude": longitude, "latitude": latitude}
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
