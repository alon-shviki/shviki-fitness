# tests/test_logout.py
def test_logout_redirects_to_index(test_client):
    """Logout should clear session and go to homepage."""
    # register + login first
    test_client.post("/register", data={
        "first_name": "Test",
        "last_name": "User",
        "national_id": "999888777",
        "email": "logout@example.com",
        "password": "1234",
        "age": "21",
        "gender": "Male",
        "subscription": "Trial"
    })
    test_client.post("/login", data={
        "email": "logout@example.com",
        "password": "1234"
    })
    response = test_client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"ShvikiFitness" in response.data or b"Login" in response.data
