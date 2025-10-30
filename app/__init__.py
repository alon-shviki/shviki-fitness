from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import OperationalError
from datetime import datetime
import time
import os
import requests

# Initialize SQLAlchemy globally
db = SQLAlchemy()


def connect_with_retry(app, retries=10, delay=3):
    """Try to connect to MySQL several times before giving up."""
    for attempt in range(retries):
        try:
            with app.app_context():
                db.engine.connect()
            print("✅ Database connection established.")
            return True
        except OperationalError:
            print(f"⏳ Database not ready, retrying in {delay}s... ({attempt + 1}/{retries})")
            time.sleep(delay)
    raise RuntimeError("❌ Could not connect to database after several attempts.")


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "super-secret-key")

    # --- Database Configuration ---
    db_user = os.environ.get("DB_USER", "shviki_user")
    db_pass = os.environ.get("DB_PASSWORD", "shviki_pass")
    db_host = os.environ.get("DB_HOST", "shviki-fitness-mysql")
    db_name = os.environ.get("DB_NAME", "shviki_db")

    if db_user and db_pass and db_host and db_name:
        app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_user}:{db_pass}@{db_host}:3306/{db_name}"
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///shviki.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
        "pool_size": 5,
        "max_overflow": 10,
    }

    db.init_app(app)

    from .models import User, UserExercise
    with app.app_context():
        connect_with_retry(app)
        db.create_all()

    # ---------------- ROUTES ---------------- #

    @app.route("/")
    def index():
        return render_template("index.html")

    # ---------- Register ---------- #
    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            if User.query.filter_by(email=request.form["email"]).first():
                flash("Email already registered", "danger")
                return redirect(url_for("register"))
            if User.query.filter_by(national_id=request.form["national_id"]).first():
                flash("National ID already registered", "danger")
                return redirect(url_for("register"))

            user = User(
                first_name=request.form["first_name"],
                last_name=request.form["last_name"],
                national_id=request.form["national_id"],
                email=request.form["email"],
                password_hash=generate_password_hash(request.form["password"]),
                age=int(request.form["age"]),
                gender=request.form["gender"],
                subscription=request.form["subscription"],
            )
            db.session.add(user)
            db.session.commit()
            session["user_id"] = user.id
            session["role"] = user.role
            return redirect(url_for("user_home"))
        return render_template("register.html")

    # ---------- Login ---------- #
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            user = User.query.filter_by(email=request.form["email"]).first()
            if user and check_password_hash(user.password_hash, request.form["password"]):
                session["user_id"] = user.id
                session["role"] = user.role
                return redirect(url_for("dashboard" if user.role == "admin" else "user_home"))
            flash("Invalid email or password", "danger")
        return render_template("login.html")

    # ---------- User Home ---------- #
    @app.route("/home")
    def user_home():
        if "user_id" not in session:
            flash("Please log in first.", "danger")
            return redirect(url_for("login"))
        classes = [
            {
                "name": "HIIT 45",
                "description": "High-intensity cardio intervals.",
                "days": "Sun, Tue, Thu",
                "time": "18:00",
                "duration": "45m",
                "level": "All",
                "coach": "Dana",
                "room": "A",
            },
            {
                "name": "Barbell Basics",
                "description": "Learn squat, bench, and deadlift safely.",
                "days": "Mon, Wed",
                "time": "19:30",
                "duration": "60m",
                "level": "Beginner",
                "coach": "Yair",
                "room": "B",
            },
        ]
        return render_template("user_home.html", classes=classes)

    # ---------- Dashboard ---------- #
    @app.route("/dashboard")
    def dashboard():
        if "user_id" not in session:
            return redirect(url_for("login"))
        if session["role"] != "admin":
            flash("Access denied.", "danger")
            return redirect(url_for("user_home"))
        users = User.query.all()
        return render_template("dashboard.html", users=users)

    # ---------- Logout ---------- #
    @app.route("/logout")
    def logout():
        session.clear()
        return redirect(url_for("index"))

    # ---------- Exercise API ---------- #
    EXERCISE_API_URL = "https://exercisedb.p.rapidapi.com"
    EXERCISE_HEADERS = {
        "x-rapidapi-key": os.environ.get("EXERCISE_API_KEY"),
        "x-rapidapi-host": os.environ.get("EXERCISE_API_HOST"),
    }

    @app.route("/exercises", methods=["GET", "POST"])
    def exercises():
        if "user_id" not in session:
            flash("Please log in to view exercises", "danger")
            return redirect(url_for("login"))

        exercise_list = []
        selected = None

        if request.method == "POST":
            query = request.form.get("muscle") or request.form.get("body_part")
            if query:
                selected = query
                normalized = query.lower().replace(" ", "-").replace("_", "-")
                endpoints = [
                    f"/exercises/name/{normalized}",
                    f"/exercises/bodyPart/{normalized}",
                    f"/exercises/target/{normalized}",
                ]

                for endpoint in endpoints:
                    response = requests.get(EXERCISE_API_URL + endpoint, headers=EXERCISE_HEADERS)
                    if response.status_code == 200:
                        data = response.json()
                        if isinstance(data, list) and data:
                            # Just create clickable Google links instead of images
                            for ex in data:
                                search_query = ex.get("name", "").replace(" ", "+")
                                ex["searchUrl"] = f"https://www.google.com/search?q={search_query}+exercise"
                            exercise_list = data
                            break
                    else:
                        print(f"[WARN] API returned {response.status_code} for {endpoint}")

        return render_template("exercises.html", exercises=exercise_list, selected=selected)

    # ---------- Save Exercise ---------- #
    @app.route("/save_exercise/<exercise_id>", methods=["POST"])
    def save_exercise(exercise_id):
        if "user_id" not in session:
            flash("Please log in to save exercises", "danger")
            return redirect(url_for("login"))

        ex = UserExercise(
            user_id=session["user_id"],
            exercise_id=exercise_id,
            exercise_name=request.form.get("name"),
            target=request.form.get("target"),
            equipment=request.form.get("equipment"),
            gif_url=request.form.get("gifUrl"),
        )
        db.session.add(ex)
        db.session.commit()
        flash("Exercise saved to your plan.", "success")
        return redirect(url_for("exercises"))

    # ---------- My Exercises ---------- #
    @app.route("/my_exercises")
    def my_exercises():
        if "user_id" not in session:
            return redirect(url_for("login"))
        saved_exercises = UserExercise.query.filter_by(user_id=session["user_id"]).all()
        return render_template("my_exercises.html", exercises=saved_exercises)

    # ---------- Delete Exercise ---------- #
    @app.route("/delete_exercise/<int:exercise_id>", methods=["POST"])
    def delete_exercise(exercise_id):
        if "user_id" not in session:
            return redirect(url_for("login"))
        ex = UserExercise.query.filter_by(id=exercise_id, user_id=session["user_id"]).first()
        if ex:
            db.session.delete(ex)
            db.session.commit()
            flash("Exercise deleted.", "info")
        return redirect(url_for("my_exercises"))

    @app.route("/health")
    def health():
     return {"status": "ok"}, 200

    return app
