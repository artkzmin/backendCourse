async def test_add_booking(authenticated_ac, db):
    room = (await db.rooms.get_all())[0]
    response = await authenticated_ac.post(
        "/bookings",
        json={"date_from": "2024-01-01", "date_to": "2024-02-02", "room_id": room.id},
    )
    assert response.status_code == 200
    res_json = response.json()
    assert isinstance(res_json, dict)
    assert res_json["status"] == "OK"
    assert "data" in res_json

    for i in range(room.quantity - 1):
        response = await authenticated_ac.post(
            "/bookings",
            json={
                "date_from": "2024-01-01",
                "date_to": "2024-02-02",
                "room_id": room.id,
            },
        )
        assert response.status_code == 200

    bad_response = await authenticated_ac.post(
        "/bookings",
        json={"date_from": "2024-01-01", "date_to": "2024-02-02", "room_id": room.id},
    )
    assert bad_response.status_code == 400
