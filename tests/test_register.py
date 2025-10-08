# tests/test_register.py
def test_register_success(test_client):
    """Register a new user successfully."""
    response = test_client.post("/register", data={
        "first_name": "Alon",
        "last_name": "Shviki",
        "national_id": "123456789",
        "email": "alon@example.com",
        "password": "1234",
        "age": "25",
        "gender": "Male",
        "subscription": "Monthly"
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Welcome" in response.data or b"Home" in response.data



def test_register_duplicate_email(test_client):
    """Block registration with an existing email."""
    # First registration
    test_client.post("/register", data={
        "first_name": "Dana",
        "last_name": "Fit",
        "national_id": "987654321",
        "email": "dana@example.com",
        "password": "5678",
        "age": "22",
        "gender": "Female",
        "subscription": "Monthly"
    })

    # Second registration with same email
    response = test_client.post("/register", data={
        "first_name": "Another",
        "last_name": "User",
        "national_id": "987654320",
        "email": "dana@example.com",
        "password": "5678",
        "age": "22",
        "gender": "Female",
        "subscription": "Monthly"
    }, follow_redirects=True)

    assert b"Email already registered" in response.data
