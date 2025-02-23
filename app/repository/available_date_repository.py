import uuid

from sqlmodel import and_, select
from app.models.available_date import AvailableDateCreate, AvailableDate
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import date


class AvailableDateRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def create_available_dates(self, create_available_date: AvailableDateCreate) -> list[AvailableDate]:
        available_date_list = AvailableDate.from_create(create_available_date)
        for available_date in available_date_list:
            self.session.add(available_date)
        await self.session.commit()
        for available_date in available_date_list:
            await self.session.refresh(available_date)
        return available_date_list


    async def get_available_dates(
            self,
            court_name: str,
            business_id: uuid.UUID,
            date: date
    ) -> list[AvailableDate]:
        query = select(AvailableDate).where(
            and_(
                AvailableDate.date==date,
                AvailableDate.court_name==court_name,
                AvailableDate.business_id==business_id
            )
        )
        available_dates = await self.session.exec(query)
        if not available_dates:
            return []
        return list(available_dates.all())


    async def delete_available_date(
            self,
            court_name: str,
            business_id: uuid.UUID,
            date: date
    ) -> None:
        query = select(AvailableDate).where(
            and_(
                AvailableDate.date==date,
                AvailableDate.court_name==court_name,
                AvailableDate.business_id==business_id
            )
        )
        available_dates = await self.session.exec(query)
        if not available_dates:
            return
        for available_date in available_dates:
            await self.session.delete(available_date)
        await self.session.commit()
        for available_date in available_dates:
            await self.session.refresh(available_date)