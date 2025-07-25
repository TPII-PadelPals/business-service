import datetime
import uuid
from typing import ClassVar

from sqlalchemy import ForeignKeyConstraint, UniqueConstraint
from sqlmodel import Field, SQLModel

from app.utilities.exceptions import NotAcceptableException

AVAILABILITY_TABLE_NAME = "padel_court_available_matches"


# Shared properties
class AvailableMatchBase(SQLModel):
    TIME_LIMIT_MIN: ClassVar[int] = 0
    TIME_LIMIT_MAX: ClassVar[int] = 23
    TIME_OF_MATCH: ClassVar[int] = 1

    court_name: str = Field(min_length=1, max_length=255, nullable=False)
    court_public_id: uuid.UUID = Field(nullable=False)
    business_public_id: uuid.UUID = Field(nullable=False)
    date: datetime.date = Field()
    initial_hour: int = Field(default=0, ge=TIME_LIMIT_MIN, le=TIME_LIMIT_MAX)

    __table_args__ = (
        ForeignKeyConstraint(
            [
                "business_public_id",
                "court_name",
                "court_public_id",
            ],  # Claves en la tabla actual
            [
                "padel_courts.business_public_id",
                "padel_courts.name",
                "padel_courts.court_public_id",
            ],  # Claves en la tabla padre
            name="fk_padel_court_unique_ref",
        ),
    )


# Properties to receive on item creation
class AvailableMatchCreate(AvailableMatchBase):
    n_matches: int = Field(default=1)

    def validate_create(self) -> None:
        if self.n_matches <= 0:
            raise NotAcceptableException("n_matches no puede ser menor a 0")
        if (
            self.n_matches * self.TIME_OF_MATCH
        ) + self.initial_hour > self.TIME_LIMIT_MAX + 1:
            raise NotAcceptableException(
                "n_matches no puede exceder el horario de un día"
            )


# Database model, database table inferred from class name
class AvailableMatch(AvailableMatchBase, table=True):
    __tablename__ = AVAILABILITY_TABLE_NAME
    reserve: bool = Field(default=False)
    id: int = Field(primary_key=True)

    __table_args__ = (
        UniqueConstraint(
            "court_name",
            "business_public_id",
            "initial_hour",
            "date",
            name="uq_available_match",
        ),
    )

    @classmethod
    def from_create(cls, create: AvailableMatchCreate) -> list["AvailableMatch"]:
        result = []
        data = create.model_dump()
        n_matches = data["n_matches"]
        for number in range(n_matches):
            available_match = cls(**data)
            available_match.initial_hour += number * cls.TIME_OF_MATCH
            result.append(available_match)
        return result

    def set_reserve(self) -> None:
        self.reserve = True

    def is_reserved(self) -> bool:
        return self.reserve


# Properties to return via API, id is always required
class AvailableMatchPublic(AvailableMatchBase):
    reserve: bool = Field(default=False)
    latitude: float = Field(nullable=False)
    longitude: float = Field(nullable=False)

    @classmethod
    def from_private(
        cls, available_match: AvailableMatch, coordinates: tuple[float, float]
    ) -> "AvailableMatchPublic":
        data = available_match.model_dump()
        data["latitude"] = coordinates[0]
        data["longitude"] = coordinates[1]
        return cls(**data)


class AvailableMatchesPublic(SQLModel):
    data: list[AvailableMatchPublic]
    count: int

    @classmethod
    def from_private(
        cls,
        available_matches_list: list[AvailableMatch],
        coordinates: tuple[float, float],
    ) -> "AvailableMatchesPublic":
        data = []
        for available_match in available_matches_list:
            data.append(AvailableMatchPublic.from_private(available_match, coordinates))
        count = len(available_matches_list)
        return cls(data=data, count=count)
