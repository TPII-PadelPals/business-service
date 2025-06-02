from app.models.padel_court import PadelCourtsPublic
from app.models.padel_court_extended import PadelCourtsPublicExtended
from app.services.business_service import BusinessService
from app.utilities.dependencies import SessionDep


class PadelCourtExtendedService:
    async def get_public_courts_extended(
        self, session: SessionDep, courts: PadelCourtsPublic
    ) -> PadelCourtsPublicExtended:
        courts_for_business = courts.get_padel_courts_for_business()
        business_service = BusinessService()
        result = PadelCourtsPublicExtended()
        for busniness_public_id, public_courts in courts_for_business.items():
            business = await business_service.get_business(session, busniness_public_id)
            for public_court in public_courts:
                result.add_court(public_court, business)
        return result
