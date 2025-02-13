import pytest


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("ivan@ivanov.ru", "password1", 200),
        ("igor@igorev.ru", "password2", 200),
        ("igor@igorev.ru", "1234", 400),
        ("bademail", "1234", 422),
    ],
)
async def test_auth_flow(email, password, status_code, ac):
    json = {"email": email, "password": password}
    reg_response = await ac.post("/auth/register", json=json)
    assert reg_response.status_code == status_code

    if reg_response.status_code != 200:
        return

    login_response = await ac.post("/auth/login", json=json)
    assert login_response.status_code == status_code
    assert ac.cookies["access_token"]

    me_response = await ac.get("/auth/me")
    assert me_response.status_code == status_code
    user = me_response.json()
    assert "password" not in user
    assert "hashed_password" not in user

    user = me_response.json()
    assert user["email"] == email
    assert user["id"]

    logout_response = await ac.post("/auth/logout")
    assert logout_response.status_code == status_code
    assert "access_token" not in ac.cookies
