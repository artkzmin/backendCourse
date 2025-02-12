import json


async def test_facilities_create_read(ac):
    # create facilities
    with open("tests/mock_facilities.json", encoding="utf-8") as f:
        facilities = json.load(f)

    for f in facilities:
        print(f"{f=}", type(f))
        response = await ac.post("/facilities", json=f)
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    # read facililities

    response = await ac.get("/facilities")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= len(facilities)
