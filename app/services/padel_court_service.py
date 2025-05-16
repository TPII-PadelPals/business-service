import uuid

from app.models.padel_court import (
    PadelCourt,
    PadelCourtFilter,
    PadelCourtsPublic,
    PadelCourtUpdate,
)
from app.repository.padel_court_repository import PadelCourtRepository
from app.utilities.dependencies import SessionDep


class PadelCourtService:
    async def get_padel_court(
        self, session: SessionDep, court_name: str, business_public_id: uuid.UUID
    ) -> PadelCourt:
        repo = PadelCourtRepository(session)
        return await repo.get_padel_court(court_name, business_public_id)

    async def get_padel_court_without_name(
        self,
        session: SessionDep,
        court_public_id: uuid.UUID,
        business_public_id: uuid.UUID,
    ) -> PadelCourt:
        repo = PadelCourtRepository(session)
        return await repo.get_padel_court_without_name(court_public_id)

    async def get_padel_courts(
        self,
        session: SessionDep,
        user_id: uuid.UUID = None,
        skip: int = 0,
        limit: int = 100,
        prov_court_filters: PadelCourtFilter = PadelCourtFilter(),
    ) -> PadelCourtsPublic:
        repo = PadelCourtRepository(session)
        filters = prov_court_filters.model_dump(exclude_unset=True, exclude_none=True)
        business_public_id = filters.pop("business_public_id", None)
        return await repo.get_padel_courts(
            business_public_id, user_id, skip, limit, **filters
        )

    async def update_padel_court(
        self,
        session: SessionDep,
        court_public_id: uuid.UUID,
        court_in: PadelCourtUpdate,
    ) -> PadelCourt:
        repo = PadelCourtRepository(session)
        court = await repo.update_padel_court(court_public_id, court_in)
        return court
