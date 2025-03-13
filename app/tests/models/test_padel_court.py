import uuid
from decimal import Decimal

import pytest

from app.models.padel_court import PadelCourt, PadelCourtPublic


async def test_public_padel_court_contains_public_id_and_not_contain_private_id() -> (
    None
):
    court_id = uuid.uuid4()
    business_id = uuid.uuid4()
    price = Decimal("150.0")
    name = "cancha pato"
    data = {
        "id": 7,
        "court_public_id": court_id,
        "name": name,
        "price_per_hour": price,
        "business_id": business_id,
    }

    padel_court = PadelCourt(**data)

    # test
    public_court = PadelCourtPublic.from_private(padel_court)

    # assert
    assert public_court is not None
    data_to_test = public_court.model_dump()

    for key in data_to_test.keys():
        assert str(data_to_test[key]) == str(data[key])

    with pytest.raises(KeyError) as _e:
        _ = data_to_test["id"]
