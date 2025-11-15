# Summary: Full Integration Test for ShvikiFitness
# Description:
# Simulates a complete user workflow using the real Flask app and test MySQL DB.
# Covers registration, login, saving an exercise, viewing saved exercises,
# and deleting the exercise to ensure end-to-end application functionality.

# tests/test_integration.py

def test_full_user_flow(test_client):
    """Simulate full user journey: register → login → save exercise → view saved exercises."""

    # ---------------------------------------
    # Step 1: Register a new user
    # ---------------------------------------
    register_response = test_client.post("/register", data={
        "first_name": "Flow",
        "last_name": "Tester",
        "national_id": "555444333",
        "email": "flow@example.com",
        "password": "1234",
        "age": "25",
        "gender": "Male",
        "subscription": "Trial"
    }, follow_redirects=True)

    assert register_response.status_code == 200
    assert b"Welcome" in register_response.data or b"Home" in register_response.data

    # ---------------------------------------
    # Step 2: Logout after registration
    # ---------------------------------------
    test_client.get("/logout", follow_redirects=True)

    # ---------------------------------------
    # Step 3: Login with the new account
    # ---------------------------------------
    login_response = test_client.post("/login", data={
        "email": "flow@example.com",
        "password": "1234"
    }, follow_redirects=True)

    assert login_response.status_code == 200
    assert b"Welcome" in login_response.data or b"Home" in login_response.data

    # ---------------------------------------
    # Step 4: Save an exercise
    # ---------------------------------------
    save_response = test_client.post("/save_exercise/321", data={
        "name": "Pull Up",
        "target": "Back",
        "equipment": "Bar",
        "gifUrl": "https://example.com/pullup.gif"
    }, follow_redirects=True)

    assert save_response.status_code == 200
    assert b"saved" in save_response.data or b"Exercise" in save_response.data

    # ---------------------------------------
    # Step 5: Retrieve saved exercises
    # ---------------------------------------
    my_exercises_response = test_client.get("/my_exercises", follow_redirects=True)

    assert my_exercises_response.status_code == 200
    assert b"Pull Up" in my_exercises_response.data or b"exercise" in my_exercises_response.data

    # ---------------------------------------
    # Step 6: Delete saved exercise
    # ---------------------------------------
    delete_response = test_client.post("/delete_exercise/1", follow_redirects=True)

    assert delete_response.status_code == 200
    assert b"deleted" in delete_response.data or b"Exercise" in delete_response.data
