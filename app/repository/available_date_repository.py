import uuid
from datetime import date

from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.available_date import AvailableDate, AvailableDateCreate
from app.utilities.exceptions import CourtAlreadyReservedException, NotFoundException


class AvailableDateRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_available_dates(
        self, create_available_date: AvailableDateCreate
    ) -> list[AvailableDate]:
        available_date_list = AvailableDate.from_create(create_available_date)
        for available_date in available_date_list:
            self.session.add(available_date)
        await self.session.commit()
        for available_date in available_date_list:
            await self.session.refresh(available_date)
        return available_date_list

    async def get_available_dates(
        self, court_name: str, business_id: uuid.UUID, date: date
    ) -> list[AvailableDate]:
        query = select(AvailableDate).where(
            and_(
                AvailableDate.date == date,
                AvailableDate.court_name == court_name,
                AvailableDate.business_id == business_id,
            )
        )
        available_dates = await self.session.exec(query)
        if available_dates is None:
            return []
        return list(available_dates.all())

    async def delete_available_date(
        self, court_name: str, business_id: uuid.UUID, date: date
    ) -> None:
        query = select(AvailableDate).where(
            and_(
                AvailableDate.date == date,
                AvailableDate.court_name == court_name,
                AvailableDate.business_id == business_id,
            )
        )
        available_dates = await self.session.exec(query)
        if available_dates is None:
            return
        for available_date in available_dates:
            await self.session.delete(available_date)
        await self.session.commit()
        for available_date in available_dates:
            await self.session.refresh(available_date)

    async def reserve_available_time(
        self,
        court_name: str,
        business_id: uuid.UUID,
        date: date,
        hour: int,
    ) -> AvailableDate:
        query = select(AvailableDate).where(
            and_(
                AvailableDate.date == date,
                AvailableDate.court_name == court_name,
                AvailableDate.business_id == business_id,
                AvailableDate.initial_hour == hour,
            )
        )
        available_date_result = await self.session.exec(query)
        available_date: AvailableDate | None = available_date_result.first()
        if available_date is None:
            raise NotFoundException("available date")
        if available_date.get_is_reserved():
            raise CourtAlreadyReservedException(court_name)
        available_date.set_reserve()
        self.session.add(available_date)
        await self.session.commit()
        await self.session.refresh(available_date)
        return available_date
