import uuid

from sqlmodel import Field, SQLModel

BUSINESS_TABLE_NAME = "businesses"


# Shared properties
class BusinessBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    location: str = Field(min_length=1, max_length=255)


# Properties to receive on item creation
class BusinessCreate(BusinessBase):
    def get_location(self) -> str:
        return self.location


# Shared private properties
class BusinessImmutable(SQLModel):
    owner_id: uuid.UUID = Field(nullable=False)
    latitude: float = Field(nullable=False)
    longitude: float = Field(nullable=False)


# Database model, database table inferred from class name
class Business(BusinessBase, BusinessImmutable, table=True):
    __tablename__ = BUSINESS_TABLE_NAME
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    def is_owned(self, user_id: uuid.UUID) -> bool:
        return self.owner_id == user_id


# Properties to return via API, id is always required
class BusinessPublic(BusinessBase, BusinessImmutable):
    id: uuid.UUID
    owner_id: uuid.UUID


class BusinessesPublic(SQLModel):
    data: list[BusinessPublic]
    count: int
