from datetime import datetime
from typing import Any

from app.models.available_match import AvailableMatch
from app.models.business import Business
from app.models.padel_court import PadelCourt


class BusinessPaseoColon:
    business_uuid = "848f4e27-5795-419a-ab67-73d46ac813ea"
    court_morning_uuid = "32b5b0a8-3813-4dcc-aba9-34d1f046a93c"
    court_morning_name = "Cancha Mañana"

    @classmethod
    def records(cls) -> list[Any]:
        return cls.business() + cls.courts() + cls.avail_matches()

    @classmethod
    def business(cls) -> list[Any]:
        business = [
            Business(
                owner_id="7904b61c-1557-4f5b-bb26-90e4bfc2bd84",
                business_public_id=cls.business_uuid,
                name="Padel Paseo Colon",
                location="Av. Paseo Colon 850, CABA",
                latitude=-34.617393884228775,
                longitude=-58.368213261883554,
            )
        ]
        return business

    @classmethod
    def courts(cls) -> list[Any]:
        courts = [
            PadelCourt(
                business_public_id=cls.business_uuid,
                court_public_id=cls.court_morning_uuid,
                name=cls.court_morning_name,
                price_per_hour=50000,
            )
        ]
        return courts

    @classmethod
    def avail_matches(cls) -> list[Any]:
        avail_matches = [
            AvailableMatch(
                business_public_id=cls.business_uuid,
                court_public_id=cls.court_morning_uuid,
                court_name=cls.court_morning_name,
                date=datetime.strptime("1/5/2025", "%d/%m/%Y").date(),
                initial_hour=9,
                reserve=False,
            )
        ]
        return avail_matches


RECORDS: list[Any] = []
RECORDS += BusinessPaseoColon().records()
