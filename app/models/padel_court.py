import uuid
from decimal import Decimal

from pydantic import field_validator
from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel

from app.models.business import BUSINESS_TABLE_NAME

PADEL_COURT_TABLE_NAME = "padel_courts"

MIN_PRICE_PER_HOUR = 0


# Shared properties
class PadelCourtBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    price_per_hour: Decimal = Field(gt=MIN_PRICE_PER_HOUR)

    @field_validator("price_per_hour", mode="before")
    def normalize_decimal(cls, v):
        v = Decimal(v)
        return Decimal(format(v, "f"))

# Properties to change
class PadelCourtUpdate(PadelCourtBase):
    pass


# Properties to receive on item creation
class PadelCourtCreate(PadelCourtBase):
    pass


class PadelCourtImmutable(SQLModel):
    court_public_id: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True)
    business_public_id: uuid.UUID = Field(
        foreign_key=f"{BUSINESS_TABLE_NAME}.business_public_id"
    )


class PadelCourt(PadelCourtBase, PadelCourtImmutable, table=True):
    __tablename__ = PADEL_COURT_TABLE_NAME
    id: int = Field(default=None, primary_key=True)

    __table_args__ = (
        UniqueConstraint(
            "name",
            "business_public_id",
            "court_public_id",
            name="uq_padel_court",
        ),
    )


# Properties to return via API, id is always required
class PadelCourtPublic(PadelCourtBase, PadelCourtImmutable):
    @classmethod
    def from_private(cls, court: PadelCourt) -> "PadelCourtPublic":
        data = court.model_dump()
        return cls(**data)


class PadelCourtsPublic(SQLModel):
    data: list[PadelCourtPublic]
    count: int

    def get_padel_courts_for_business(self) -> dict[uuid.UUID, list[PadelCourtPublic]]:
        result = {}
        for court in self.data:
            business_public_id = court.business_public_id
            courts_by_business = result.get(business_public_id)
            if courts_by_business is not None:
                courts_by_business.append(court)
            else:
                result[business_public_id] = [court]
        return result


class PadelCourtFilter(SQLModel):
    name: str | None = Field(min_length=1, max_length=255, default=None)
    price_per_hour: Decimal | None = Field(gt=MIN_PRICE_PER_HOUR, default=None)
    court_public_id: uuid.UUID | None = None
    business_public_id: uuid.UUID | None = None

    def is_valid_filter_for_business_public_id(
        self, owner_id: uuid.UUID | None
    ) -> bool:
        return (self.business_public_id is None) != (owner_id is None)
