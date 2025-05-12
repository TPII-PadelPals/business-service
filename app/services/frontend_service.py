from app.core.config import settings

from .base_service import BaseService


class FrontendService(BaseService):
    def __init__(self):
        """Init the service."""
        super().__init__()
        self._set_base_url(
            settings.FRONTEND_SERVICE_HTTP,
            settings.FRONTEND_SERVICE_HOST,
            settings.FRONTEND_SERVICE_PORT,
        )
