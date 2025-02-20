import uuid

from typing import ClassVar
from sqlalchemy import BIGINT
from sqlmodel import Field, SQLModel
from datetime import date


AVAILABILITY_TABLE_NAME = "padel_court_available_date"


# Shared properties
class AvailableDateBase(SQLModel):
    TIME_LIMIT_MIN:ClassVar[int] = 0
    TIME_LIMIT_MAX:ClassVar[int] = 23
    
    date: date = Field()
    initial_hour: int = Field(default=0, ge=TIME_LIMIT_MIN, le=TIME_LIMIT_MAX)


# Properties to receive on item creation
class AvailableDateCreate(AvailableDateBase):
    number_of_games: int = Field(default=0)


# private arguments
class AvailableDatePrivate(AvailableDateBase):
    id: BIGINT = Field(primary_key=True)


# Properties to receive on item update
class AvailableDateBaseUpdate(AvailableDateBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore[assignment]


# Database model, database table inferred from class name
class AvailableDate(AvailableDateBase, AvailableDatePrivate, table=True):
    __tablename__ = AVAILABILITY_TABLE_NAME

# Properties to return via API, id is always required
class AvailableDatePublic(AvailableDateBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class AvailableDatesPublic(SQLModel):
    data: list[AvailableDatePublic]
    count: int