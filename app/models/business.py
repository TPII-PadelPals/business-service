import uuid

from sqlmodel import Field, SQLModel


# Shared properties
class BusinessBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    location: str | None = Field(min_length=1, max_length=255)


# Properties to receive on item creation
class BusinessCreate(BusinessBase):
    pass


# Properties to receive on Business update
# class BusinessUpdate(BusinessBase):
#     name: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore[assignment]


# Database model, database table inferred from class name
class Business(BusinessBase, table=True):
    __tablename__ = "businesses"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    location: str = Field(default="")


# Properties to return via API, id is always required
class BusinessPublic(BusinessBase):
    id: uuid.UUID


# class BusinesssesPublic(SQLModel):
#     data: list[BusinessPublic]
#     count: int
