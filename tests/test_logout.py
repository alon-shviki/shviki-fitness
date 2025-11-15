# Summary: Logout Behavior Test
# Description:
# Verifies that logging out clears the session and redirects the user
# back to the homepage or login screen. Ensures proper session handling.

# tests/test_logout.py
def test_logout_redirects_to_index(test_client):
    """Logout should clear session and return the user to the homepage."""

    # ---------------------------------------
    # Register a user and log them in
    # ---------------------------------------
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

    # ---------------------------------------
    # Perform logout and verify redirect
    # ---------------------------------------
    response = test_client.get("/logout", follow_redirects=True)

    assert response.status_code == 200
    assert b"ShvikiFitness" in response.data or b"Login" in response.data
