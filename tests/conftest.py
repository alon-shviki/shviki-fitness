import pytest
import os
from app import create_app, db
from app.models import User

@pytest.fixture(scope="module")
def test_client():
    """Create a Flask test client connected to the correct MySQL DB."""
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        "mysql+pymysql://shviki_user:shviki_pass@db:3306/shviki_db"
    )

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            # 🧹 Cleanup only in GitHub Actions (safe)
            if os.getenv("GITHUB_ACTIONS") == "true":
                db.session.remove()
                db.drop_all()

@pytest.fixture(autouse=True)
def clean_test_users():
    """
    Automatically delete test users after each test.
    Runs after each test function.
    Never drops tables, only deletes test accounts.
    """
    yield
    test_emails = ["alon@example.com", "dana@example.com", "test@example.com"]
    for email in test_emails:
        user = User.query.filter_by(email=email).first()
        if user:
            db.session.delete(user)
    db.session.commit()
