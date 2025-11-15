# Summary: Database Models for Users and Exercises
# Description:
# This file defines the SQLAlchemy ORM models for application users and 
# their saved exercises. It includes the User model, the UserExercise model, 
# and the relationship linking them together.

from datetime import datetime
from . import db


# ------------------------------
# User Model
# Stores personal details, login data,
# subscription type, and user role.
# ------------------------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    national_id = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    subscription = db.Column(db.String(50))
    role = db.Column(db.String(20), default="user")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to saved exercises
    exercises = db.relationship(
        "UserExercise",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# ------------------------------
# UserExercise Model
# Stores exercises saved by users,
# including metadata like target muscle,
# equipment, and creation timestamp.
# ------------------------------
class UserExercise(db.Model):
    __tablename__ = "user_exercises"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    exercise_id = db.Column(db.String(50), nullable=False)
    exercise_name = db.Column(db.String(255), nullable=False)
    target = db.Column(db.String(100))
    equipment = db.Column(db.String(100))
    gif_url = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Back-reference to User
    user = db.relationship("User", back_populates="exercises")
