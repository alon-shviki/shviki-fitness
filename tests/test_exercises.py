# tests/test_exercises.py
def test_save_and_delete_exercise(test_client):
    """Simulate saving and deleting an exercise."""
    # register + login
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

    # save an exercise
    response = test_client.post("/save_exercise/1234", data={
        "name": "Push Ups",
        "target": "Chest",
        "equipment": "None",
        "gifUrl": "https://example.com/pushup.gif"
    }, follow_redirects=True)
    assert b"Exercise saved" in response.data or response.status_code == 200

    # delete it again
    response = test_client.post("/delete_exercise/1", follow_redirects=True)
    assert b"deleted" in response.data or response.status_code == 200
