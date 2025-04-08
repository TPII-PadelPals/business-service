import datetime
import uuid

from app.models.available_match import (
    AvailableMatchCreate,
    AvailableMatchesPublic,
    AvailableMatchPublic,
)
from app.services.available_match_service import AvailableMatchService
from app.services.business_service import BusinessService
from app.utilities.dependencies import SessionDep


class AvailableMatchServicePublic:
    def __init__(self) -> None:
        self.service_available_match = AvailableMatchService()
        self.business_service = BusinessService()

    async def create_available_matches_in_date(
        self,
        session: SessionDep,
        user_id: uuid.UUID,
        court_name: str,
        business_public_id: uuid.UUID,
        available_match_in: AvailableMatchCreate,
    ) -> AvailableMatchesPublic:
        available_matches = (
            await self.service_available_match.create_available_matches_in_date(
                session, user_id, court_name, business_public_id, available_match_in
            )
        )
        business = await self.business_service.get_business(session, business_public_id)
        return AvailableMatchesPublic.from_private(
            available_matches, business.get_coordinates()
        )

    async def get_available_matches_in_date(
        self,
        session: SessionDep,
        court_name: str,
        business_public_id: uuid.UUID,
        date: datetime.date,
    ) -> AvailableMatchesPublic:
        available_matches = (
            await self.service_available_match.get_available_matches_in_date(
                session, court_name, business_public_id, date
            )
        )
        business = await self.business_service.get_business(session, business_public_id)
        return AvailableMatchesPublic.from_private(
            available_matches, business.get_coordinates()
        )

    async def reserve_available_match(
        self,
        session: SessionDep,
        court_name: str,
        business_public_id: uuid.UUID,
        date: datetime.date,
        hour: int,
    ) -> AvailableMatchPublic:
        available_match = await self.service_available_match.reserve_available_match(
            session, court_name, business_public_id, date, hour
        )
        business = await self.business_service.get_business(session, business_public_id)
        return AvailableMatchPublic.from_private(
            available_match, business.get_coordinates()
        )
