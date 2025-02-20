import uuid
import datetime

from sqlalchemy import UniqueConstraint
from typing import ClassVar
from sqlmodel import Field, SQLModel

from app.utilities.exceptions import NotAcceptableException

AVAILABILITY_TABLE_NAME = "padel_court_available_date"


# Shared properties
class AvailableDateBase(SQLModel):
    TIME_LIMIT_MIN: ClassVar[int] = 0
    TIME_LIMIT_MAX: ClassVar[int] = 23
    TIME_OF_GAME: ClassVar[int] = 1

    court_id: int = Field(foreign_key="padel_courts.id", ondelete="CASCADE")
    business_id: uuid.UUID = Field(foreign_key="businesses.id", ondelete="CASCADE")
    date: datetime.date = Field()
    initial_hour: int = Field(default=0, ge=TIME_LIMIT_MIN, le=TIME_LIMIT_MAX)


# Properties to receive on item creation
class AvailableDateCreate(AvailableDateBase):
    number_of_games: int = Field(default=1)


    def validate_create(self) -> None:
        if self.number_of_games <= 0:
            raise NotAcceptableException("number_of_games cannot be less than 0")
        if (self.number_of_games * self.TIME_OF_GAME) + self.initial_hour > self.TIME_LIMIT_MAX + 1:
            raise NotAcceptableException("number_of_games cannot exceed the time of one day")


# Private and in-mutable properties
class AvailableDateImmutable(SQLModel):
    id: int = Field(primary_key=True)


# Database model, database table inferred from class name
class AvailableDate(AvailableDateBase, AvailableDateImmutable, table=True):
    __tablename__ = AVAILABILITY_TABLE_NAME
    is_reserved: bool = Field(default=False)


    __table_args__ = (
        UniqueConstraint(
            "court_id",
            "business_id",
            "initial_hour",
            "date",
            name="uq_available_date",
        ),
    )


    def _increment_initial_hour(self, increment: int) -> None:
        self.initial_hour += increment


    @classmethod
    def from_create(cls, create: AvailableDateCreate) -> list["AvailableDate"]:
        result = []
        data = create.model_dump()
        number_of_games = data['number_of_games']
        # data["is_reserved"] = False
        for i_game in range(number_of_games):
            available_date = cls(**data)
            increment = i_game * cls.TIME_OF_GAME
            available_date._increment_initial_hour(increment)
            result.append(available_date)
        return result


    def set_reserve(self) -> None:
        self.is_reserved = True


    # def get_is_reserved(self):
    #     return self.is_reserved


# Properties to return via API, id is always required
class AvailableDatePublic(AvailableDateBase):
    is_reserved: bool = Field(default=False)


    @classmethod
    def from_private(cls, available_day: AvailableDate) -> "AvailableDatePublic":
        data = available_day.model_dump()
        return cls(**data)


class AvailableDatesPublic(SQLModel):
    data: list[AvailableDatePublic]
    count: int


    @classmethod
    def from_private(
            cls, available_day_list: list[AvailableDate]
    ) -> "AvailableDatesPublic":
        data = []
        for match_player in available_day_list:
            data.append(AvailableDatePublic.from_private(match_player))
        count = len(available_day_list)
        return cls(data=data, count=count)