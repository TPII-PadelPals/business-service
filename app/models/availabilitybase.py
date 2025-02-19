import uuid

from sqlmodel import Field, SQLModel


AVAILABILITY_TABLE_NAME = "padel_court_availability"


# Shared properties
class AvailabilityBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class AvailabilityBaseCreate(AvailabilityBase):
    pass


# Properties to receive on item update
class AvailabilityBaseUpdate(AvailabilityBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore[assignment]


# Database model, database table inferred from class name
class Availability(AvailabilityBase, table=True):
    __tablename__ = AVAILABILITY_TABLE_NAME
    id: int = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(nullable=False, index=True)


# Properties to return via API, id is always required
class AvailabilityPublic(AvailabilityBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[AvailabilityPublic]
    count: int