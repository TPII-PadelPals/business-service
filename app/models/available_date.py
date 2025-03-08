import datetime
import uuid
from typing import ClassVar

from sqlalchemy import ForeignKeyConstraint, UniqueConstraint
from sqlmodel import Field, SQLModel

from app.utilities.exceptions import NotAcceptableException

AVAILABILITY_TABLE_NAME = "padel_court_available_dates"


# Shared properties
class AvailableMatchBase(SQLModel):
    TIME_LIMIT_MIN: ClassVar[int] = 0
    TIME_LIMIT_MAX: ClassVar[int] = 23
    TIME_OF_MATCH: ClassVar[int] = 1

    court_name: str = Field(min_length=1, max_length=255, nullable=False)
    business_id: uuid.UUID = Field(nullable=False)
    date: datetime.date = Field()
    initial_hour: int = Field(default=0, ge=TIME_LIMIT_MIN, le=TIME_LIMIT_MAX)

    __table_args__ = (
        ForeignKeyConstraint(
            ["business_id", "court_name"],  # Claves en la tabla actual
            [
                "padel_courts.business_id",
                "padel_courts.name",
            ],  # Claves en la tabla padre
            name="fk_padel_court_unique_ref",
        ),
    )


# Properties to receive on item creation
class AvailableMatchCreate(AvailableMatchBase):
    n_matches: int = Field(default=1)

    def validate_create(self) -> None:
        if self.n_matches <= 0:
            raise NotAcceptableException("n_matches cannot be less than 0")
        if (
            self.n_matches * self.TIME_OF_MATCH
        ) + self.initial_hour > self.TIME_LIMIT_MAX + 1:
            raise NotAcceptableException("n_matches cannot exceed the time of one day")


# Database model, database table inferred from class name
class AvailableMatch(AvailableMatchBase, table=True):
    __tablename__ = AVAILABILITY_TABLE_NAME
    reserve: bool = Field(default=False)
    id: int = Field(primary_key=True)

    __table_args__ = (
        UniqueConstraint(
            "court_name",
            "business_id",
            "initial_hour",
            "date",
            name="uq_available_date",
        ),
    )

    def _increment_initial_hour(self, increment: int) -> None:
        self.initial_hour += increment

    @classmethod
    def from_create(cls, create: AvailableMatchCreate) -> list["AvailableMatch"]:
        result = []
        data = create.model_dump()
        n_matches = data["n_matches"]
        for number in range(n_matches):
            available_date = cls(**data)
            increment = number * cls.TIME_OF_MATCH
            available_date._increment_initial_hour(increment)
            result.append(available_date)
        return result

    def set_reserve(self) -> None:
        self.reserve = True

    def is_reserved(self) -> bool:
        return self.reserve


# Properties to return via API, id is always required
class AvailableMatchPublic(AvailableMatchBase):
    reserve: bool = Field(default=False)

    @classmethod
    def from_private(cls, available_day: AvailableMatch) -> "AvailableMatchPublic":
        data = available_day.model_dump()
        return cls(**data)


class AvailableDatesPublic(SQLModel):
    data: list[AvailableMatchPublic]
    count: int

    @classmethod
    def from_private(
        cls, available_day_list: list[AvailableMatch]
    ) -> "AvailableDatesPublic":
        data = []
        for available_day in available_day_list:
            data.append(AvailableMatchPublic.from_private(available_day))
        count = len(available_day_list)
        return cls(data=data, count=count)
