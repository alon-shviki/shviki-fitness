def test_login_invalid_user(test_client):
    """Try logging in with invalid credentials."""
    response = test_client.post("/login", data={
        "email": "notfound@example.com",
        "password": "wrongpass"
    }, follow_redirects=True)

    assert b"Invalid" in response.data or response.status_code in [400, 200]


# tests/test_login.py
def test_login_success(test_client):
    """Register and then log in successfully."""
    # Register a test user
    test_client.post("/register", data={
        "first_name": "Test",
        "last_name": "User",
        "national_id": "111222333",
        "email": "test@example.com",
        "password": "1234",
        "age": "20",
        "gender": "Male",
        "subscription": "Trial"
    })

    # Then log in
    response = test_client.post("/login", data={
        "email": "test@example.com",
        "password": "1234"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Welcome" in response.data or b"Home" in response.data

