import uuid

from app.models.business import Business


async def test_is_a_owner() -> None:
    owner_id = uuid.uuid4()
    data = {
        "business_public_id": uuid.uuid4(),
        "owner_id": owner_id,
        "name": "NAME",
        "location": "LOCATION",
    }
    business = Business(**data)
    # assert
    assert business.is_owned(owner_id)


async def test_not_is_a_owner() -> None:
    owner_id = uuid.uuid4()
    not_owner_id = uuid.uuid4()
    limit = 100  # caso donde siempre es igual
    while owner_id == not_owner_id:
        not_owner_id = uuid.uuid4()
        limit -= 1
        assert limit != 0
    data = {
        "business_public_id": uuid.uuid4(),
        "owner_id": owner_id,
        "name": "NAME",
        "location": "LOCATION",
    }
    business = Business(**data)
    # assert
    assert not business.is_owned(not_owner_id)
