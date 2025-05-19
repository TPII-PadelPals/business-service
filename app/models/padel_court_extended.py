from sqlmodel import Field, SQLModel

from app.models.business import Business, BusinessImmutable
from app.models.padel_court import PadelCourtPublic


# Properties to return via API, id is always required
class PadelCourtPublicExtended(PadelCourtPublic, BusinessImmutable):
    business_name: str = Field(min_length=1, max_length=255)
    business_location: str = Field(min_length=1, max_length=255)


class PadelCourtsPublicExtended(SQLModel):
    data: list[PadelCourtPublicExtended] = []
    count: int = 0

    def add_court(self, court: PadelCourtPublic, business: Business) -> None:
        data_business = business.model_dump()
        data = {
            "business_name": data_business.pop("name"),
            "business_location": data_business.pop("location"),
        }
        data.update(data_business)
        data.update(court.model_dump())
        new_court = PadelCourtPublicExtended(**data)
        self.data.append(new_court)
        self.count += 1
