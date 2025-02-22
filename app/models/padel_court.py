import uuid
from decimal import Decimal

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel

from app.models.business import BUSINESS_TABLE_NAME

PADEL_COURT_TABLE_NAME = "padel_courts"

MIN_PRICE_PER_HOUR = 0


# Shared properties
class PadelCourtBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    price_per_hour: Decimal = Field(gt=MIN_PRICE_PER_HOUR)


# Properties to receive on item creation
class PadelCourtCreate(PadelCourtBase):
    pass


class PadelCourt(PadelCourtBase, table=True):
    __tablename__ = PADEL_COURT_TABLE_NAME
    id: int = Field(default=None, primary_key=True)
    business_id: uuid.UUID = Field(foreign_key=f"{BUSINESS_TABLE_NAME}.id")


    __table_args__ = (
        UniqueConstraint(
            "name",
            "business_id",
            name="uq_padel_court",
        ),
    )


# Properties to return via API, id is always required
class PadelCourtPublic(PadelCourtBase):
    business_id: uuid.UUID
