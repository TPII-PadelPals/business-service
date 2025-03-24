from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.owner import Owner, OwnerCreate


class OwnerRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_owner(self, owner_in: OwnerCreate) -> Owner:
        new_owner = Owner.model_validate(owner_in)
        self.session.add(new_owner)
        await self.session.commit()
        await self.session.refresh(new_owner)
        return new_owner
