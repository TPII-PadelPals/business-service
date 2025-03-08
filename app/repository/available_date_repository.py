import uuid
from datetime import date

from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.available_date import AvailableMatch, AvailableMatchCreate
from app.utilities.exceptions import CourtAlreadyReservedException, NotFoundException


class AvailableDateRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_available_matchs_in_date(
        self, create_available_date: AvailableMatchCreate
    ) -> list[AvailableMatch]:
        available_date_list = AvailableMatch.from_create(create_available_date)
        for available_date in available_date_list:
            self.session.add(available_date)
        await self.session.commit()
        for available_date in available_date_list:
            await self.session.refresh(available_date)
        return available_date_list

    async def get_available_matchs_in_date(
        self, court_name: str, business_id: uuid.UUID, date: date
    ) -> list[AvailableMatch]:
        query = select(AvailableMatch).where(
            and_(
                AvailableMatch.date == date,
                AvailableMatch.court_name == court_name,
                AvailableMatch.business_id == business_id,
            )
        )
        available_dates = await self.session.exec(query)
        if available_dates is None:
            return []
        return list(available_dates.all())

    async def delete_available_matchs_in_date(
        self, court_name: str, business_id: uuid.UUID, date: date
    ) -> None:
        query = select(AvailableMatch).where(
            and_(
                AvailableMatch.date == date,
                AvailableMatch.court_name == court_name,
                AvailableMatch.business_id == business_id,
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

    async def get_available_match(
            self,
            court_name: str,
            business_id: uuid.UUID,
            date: date,
            hour: int,
    ) -> AvailableMatch:
        query = select(AvailableMatch).where(
            and_(
                AvailableMatch.date == date,
                AvailableMatch.court_name == court_name,
                AvailableMatch.business_id == business_id,
                AvailableMatch.initial_hour == hour,
                )
        )
        available_date_result = await self.session.exec(query)
        available_date: AvailableMatch | None = available_date_result.first()
        if available_date is None:
            raise NotFoundException("available date")
        return available_date

    async def update_available_match(self, available_match: AvailableMatch) -> AvailableMatch:
        self.session.add(available_match)
        await self.session.commit()
        await self.session.refresh(available_match)
        return available_match
