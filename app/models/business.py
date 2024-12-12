import uuid

from sqlmodel import Field, SQLModel

BUSINESS_TABLE_NAME = "businesses"


# Shared properties
class BusinessBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    location: str = Field(min_length=1, max_length=255)


# Properties to receive on item creation
class BusinessCreate(BusinessBase):
    pass


# Database model, database table inferred from class name
class Business(BusinessBase, table=True):
    __tablename__ = BUSINESS_TABLE_NAME
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)


# Properties to return via API, id is always required
class BusinessPublic(BusinessBase):
    id: uuid.UUID
