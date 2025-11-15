# Summary: Pytest Configuration for Flask Application
# Description:
# Provides reusable pytest fixtures for setting up a Flask test client,
# initializing a temporary MySQL-backed test database, and cleaning up
# test user records after each test. Ensures all tests run in isolation.

import pytest
import os
from app import create_app, db
from app.models import User


# -------------------------------------------
# Test Client Fixture
# Creates a Flask test client and initializes
# a temporary database for running tests.
# -------------------------------------------
@pytest.fixture(scope="module")
def test_client():
    """Create a Flask test client connected to the correct MySQL DB."""
    app = create_app()
    app.config["TESTING"] = True

    # Database connection for tests (MySQL inside GitHub Actions)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "mysql+pymysql://shviki_user:shviki_pass@db:3306/shviki_db"
    )

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client

            # Cleanup database only when running inside GitHub Actions
            if os.getenv("GITHUB_ACTIONS") == "true":
                db.session.remove()
                db.drop_all()


# -------------------------------------------
# Auto-Cleanup Fixture
# Runs after every test and removes any test
# user accounts created during testing.
# Ensures database isolation between tests.
# -------------------------------------------
@pytest.fixture(autouse=True)
def clean_test_users():
    """
    Automatically delete test users after each test.
    Never drops tables; only removes records created during tests.
    """
    yield

    test_emails = ["alon@example.com", "dana@example.com", "test@example.com"]

    for email in test_emails:
        user = User.query.filter_by(email=email).first()
        if user:
            db.session.delete(user)

    db.session.commit()
