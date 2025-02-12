import json


async def test_facilities(ac):
    # create facilities
    with open("tests/mock_facilities.json", encoding="utf-8") as f:
        facilities = json.load(f)

    for f in facilities:
        print(f"{f=}", type(f))
        response = await ac.post("/facilities/", json=f)
        assert response.status_code == 200

    # read facililities

    response = await ac.get("/facilities/")
    assert response.status_code == 200
    assert len(response.json()) >= len(facilities)
