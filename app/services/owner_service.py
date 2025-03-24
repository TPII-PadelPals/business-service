from sqlalchemy.exc import IntegrityError

from app.models.owner import Owner, OwnerCreate
from app.repository.owner_repository import OwnerRepository
from app.utilities.dependencies import SessionDep
from app.utilities.exceptions import NotUniqueException


class OwnerService:
    async def create_owner(self, session: SessionDep, owner: OwnerCreate) -> Owner:
        repo = OwnerRepository(session)
        try:
            new_owner = await repo.create_owner(owner)
        except IntegrityError:
            await session.rollback()
            raise NotUniqueException("Owner")
        except Exception as e:
            await session.rollback()
            raise e
        return new_owner
