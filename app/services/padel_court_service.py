#######################################################################################################################
# IMPORTANTE EN LA US-177 NO SE HARA EL REFACTOR PARA PASAR LAS COSAS DEL ROUTES AL SERVICE ESTO SE HARA EN LA US-283 #
# EN ESTA US SOLO SE AGREGARA LAS COSAS QUE SON NESESARIAS PARA LA PROPIA US-177                                      #
#######################################################################################################################
import uuid

from app.models.padel_court import PadelCourt
from app.repository.padel_court_repository import PadelCourtRepository
from app.utilities.dependencies import SessionDep


class PadelCourtService:
    async def get_padel_court(self, session: SessionDep, court_name: str, business_id: uuid.UUID) -> PadelCourt:
        repo = PadelCourtRepository(session)
        return await repo.get_padel_court(court_name, business_id)