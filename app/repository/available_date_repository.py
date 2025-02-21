from app.models.available_date import AvailableDateCreate, AvailableDate


class AvailableDateRepository:
    def __init__(self, session):
        self.session = session


    async def create_available_dates(self, create_available_date: AvailableDateCreate) -> list[AvailableDate]:
        available_date_list = AvailableDate.from_create(create_available_date)
        for available_date in available_date_list:
            self.session.add(available_date)
        await self.session.commit()
        for available_date in available_date_list:
            await self.session.refresh(available_date)
        return available_date_list