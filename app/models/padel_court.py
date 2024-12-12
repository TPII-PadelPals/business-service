import uuid
from decimal import Decimal

from sqlmodel import Field, SQLModel

from app.models.business import BUSINESS_TABLE_NAME

PADEL_COURT_TABLE_NAME = "padel_courts"


# Shared properties
class PadelCourtBase(SQLModel):
    name: str = Field(..., min_length=1, max_length=255)
    price_per_hour: Decimal = Field(...)


# Properties to receive on item creation
class PadelCourtCreate(PadelCourtBase):
    pass


class PadelCourt(PadelCourtBase, table=True):
    __tablename__ = PADEL_COURT_TABLE_NAME
    id: int = Field(default=None, primary_key=True)
    business_id: uuid.UUID = Field(foreign_key=f"{BUSINESS_TABLE_NAME}.id")


# Properties to return via API, id is always required
class PadelCourtPublic(PadelCourtBase):
    id: int
    business_id: uuid.UUID
