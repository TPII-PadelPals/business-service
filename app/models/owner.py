import uuid

from sqlmodel import Field, SQLModel

OWNER_TABLE_NAME = "owners"


class OwnerBase(SQLModel):
    user_public_id: uuid.UUID = Field(default_factory=uuid.uuid4, unique=True)
    password_hash: str = Field(min_length=1, max_length=255)


class OwnerCreate(OwnerBase):
    pass


class OwnerImmutable(SQLModel):
    pass


class OwnerUpdate(OwnerBase):
    pass


class Owner(OwnerBase, OwnerImmutable, table=True):
    __tablename__ = OWNER_TABLE_NAME
    id: int = Field(default=None, primary_key=True)


class OwnerPublic(OwnerBase, OwnerImmutable):
    @classmethod
    def from_public(cls, owner: Owner) -> "OwnerPublic":
        return cls(**owner.model_dump())


class OwnersPublic(SQLModel):
    data: list[OwnerPublic]
    count: int
