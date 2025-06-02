import uuid
from datetime import date

from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.available_match import AvailableMatch, AvailableMatchCreate
from app.utilities.exceptions import NotFoundException


class AvailableMatchesRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_available_matches_in_date(
        self, create_available_date: AvailableMatchCreate
    ) -> list[AvailableMatch]:
        available_matches_list = AvailableMatch.from_create(create_available_date)
        for available_match in available_matches_list:
            self.session.add(available_match)
        await self.session.commit()
        for available_match in available_matches_list:
            await self.session.refresh(available_match)
        return available_matches_list

    async def get_available_matches_in_date(
        self, court_name: str, business_public_id: uuid.UUID, date: date
    ) -> list[AvailableMatch]:
        query = select(AvailableMatch).where(
            and_(
                AvailableMatch.date == date,
                AvailableMatch.court_name == court_name,
                AvailableMatch.business_public_id == business_public_id,
            )
        )
        available_matches = await self.session.exec(query)
        if available_matches is None:
            return []
        return list(available_matches.all())

    async def delete_available_matches_in_date(
        self, court_name: str, business_public_id: uuid.UUID, date: date
    ) -> None:
        query = select(AvailableMatch).where(
            and_(
                AvailableMatch.date == date,
                AvailableMatch.court_name == court_name,
                AvailableMatch.business_public_id == business_public_id,
            )
        )
        available_matches = await self.session.exec(query)
        if available_matches is None:
            return
        for available_match in available_matches:
            await self.session.delete(available_match)
        await self.session.commit()
        for available_match in available_matches:
            await self.session.refresh(available_match)

    async def get_available_match(
        self,
        court_name: str,
        business_public_id: uuid.UUID,
        date: date,
        hour: int,
    ) -> AvailableMatch:
        query = select(AvailableMatch).where(
            and_(
                AvailableMatch.date == date,
                AvailableMatch.court_name == court_name,
                AvailableMatch.business_public_id == business_public_id,
                AvailableMatch.initial_hour == hour,
            )
        )
        available_date_result = await self.session.exec(query)
        available_date: AvailableMatch | None = available_date_result.first()
        if available_date is None:
            raise NotFoundException("Disponibilidad para el match")
        return available_date

    async def update_available_match(
        self, available_match: AvailableMatch
    ) -> AvailableMatch:
        update_dict = available_match.model_dump(exclude_unset=True)
        available_match.sqlmodel_update(update_dict)
        self.session.add(available_match)
        await self.session.commit()
        await self.session.refresh(available_match)
        return available_match
