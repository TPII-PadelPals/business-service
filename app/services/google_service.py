from typing import Any

from app.core.config import settings
from app.utilities.exceptions import ExternalServiceException

from .base_service import BaseService


class GoogleService(BaseService):
    def __init__(self) -> None:
        """Init the service."""
        super().__init__()

    async def get_coordinates(self, address: str) -> Any:
        """Get address coordinates using google address validation api."""
        ADDRESS_VALIDATION_HOST = "addressvalidation.googleapis.com"
        ADDRESS_VALIDATION_PATH = "/v1:validateAddress"

        if not address:
            raise ExternalServiceException(
                service_name="google-address", detail="Invalid location"
            )

        self._set_base_url(ADDRESS_VALIDATION_HOST)
        json_data = {
            "address": {"regionCode": "AR", "addressLines": [address]},
        }
        q_params = {
            "key": settings.GOOGLE_API_KEY,
        }
        response = await self.post(
            ADDRESS_VALIDATION_PATH, json=json_data, params=q_params
        )
        if response is None:
            raise ExternalServiceException(
                service_name="google-address",
                detail="Failed to fetch coordinates from Google",
            )

        if "result" not in response or "geocode" not in response["result"]:
            raise ExternalServiceException(
                service_name="google-address", detail="Invalid location"
            )

        coordinates = response["result"]["geocode"]["location"]
        longitude = coordinates["longitude"]
        latitude = coordinates["latitude"]

        return longitude, latitude
