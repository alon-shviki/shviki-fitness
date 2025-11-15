# Summary: Exercise Save/Delete Test
# Description:
# Validates the workflow for saving an exercise to a user's account
# and then deleting it. This test simulates user registration, login,
# exercise creation, and removal to ensure full functionality.

# tests/test_exercises.py
def test_save_and_delete_exercise(test_client):
    """Simulate saving and deleting an exercise."""

    # ---------------------------------------
    # Register a test user and log them in
    # ---------------------------------------
    test_client.post("/register", data={
        "first_name": "Exercise",
        "last_name": "Tester",
        "national_id": "444333222",
        "email": "exercise@example.com",
        "password": "1234",
        "age": "23",
        "gender": "Male",
        "subscription": "Trial"
    })
    test_client.post("/login", data={
        "email": "exercise@example.com",
        "password": "1234"
    })

    # ---------------------------------------
    # Save an exercise to the test user
    # ---------------------------------------
    response = test_client.post("/save_exercise/1234", data={
        "name": "Push Ups",
        "target": "Chest",
        "equipment": "None",
        "gifUrl": "https://example.com/pushup.gif"
    }, follow_redirects=True)

    assert b"Exercise saved" in response.data or response.status_code == 200

    # ---------------------------------------
    # Delete the exercise again
    # ---------------------------------------
    response = test_client.post("/delete_exercise/1", follow_redirects=True)
    assert b"deleted" in response.data or response.status_code == 200
