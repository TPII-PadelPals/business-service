import uuid

from sqlmodel import Field, SQLModel


AVAILABILITY_TABLE_NAME = "padel_court_available_date"


# Shared properties
class AvailableDateBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class AvailableDateCreate(AvailableDateBase):
    pass


# Properties to receive on item update
class AvailableDateBaseUpdate(AvailableDateBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore[assignment]


# Database model, database table inferred from class name
class AvailableDate(AvailableDateBase, table=True):
    __tablename__ = AVAILABILITY_TABLE_NAME
    id: int = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(nullable=False, index=True)


# Properties to return via API, id is always required
class AvailableDatePublic(AvailableDateBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class AvailableDatesPublic(SQLModel):
    data: list[AvailableDatePublic]
    count: int