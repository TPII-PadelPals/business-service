#######################################################################################################################
# IMPORTANTE EN LA US-177 NO SE HARA EL REFACTOR PARA PASAR LAS COSAS DEL ROUTES AL SERVICE ESTO SE HARA EN LA US-283 #
# EN ESTA US SOLO SE AGREGARA LAS COSAS QUE SON NESESARIAS PARA LA PROPIA US-177                                      #
#######################################################################################################################
import uuid

from app.models.business import Business
from app.repository.business_repository import BusinessRepository
from app.utilities.dependencies import SessionDep


class BusinessService:
    async def get_business(
        self, session: SessionDep, business_id: uuid.UUID
    ) -> Business:
        repo = BusinessRepository(session)
        return await repo.get_business(business_id)
