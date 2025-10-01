from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import requests

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "super-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI", "sqlite:///shviki.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .models import User, UserExercise

    with app.app_context():
        db.create_all()

    # ------------------ ROUTES ------------------

    @app.route('/')
    def index():
        return render_template('index.html')

    # Register
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            if User.query.filter_by(email=request.form['email']).first():
                flash("Email already registered", "danger")
                return redirect(url_for('register'))
            if User.query.filter_by(national_id=request.form['national_id']).first():
                flash("National ID already registered", "danger")
                return redirect(url_for('register'))

            user = User(
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                national_id=request.form['national_id'],
                email=request.form['email'],
                password_hash=generate_password_hash(request.form['password']),
                age=int(request.form['age']),
                gender=request.form['gender'],
                subscription=request.form['subscription']
            )
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            session['role'] = user.role
            return redirect(url_for('user_home'))
        return render_template('register.html')

    # Login
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            user = User.query.filter_by(email=request.form['email']).first()

            if user and check_password_hash(user.password_hash, request.form['password']):
                session['user_id'] = user.id
                session['role'] = user.role
                if user.role == 'admin':
                    return redirect(url_for('dashboard'))
                else:
                    return redirect(url_for('user_home'))
            else:
                flash("Invalid email or password", "danger")

        return render_template('login.html')

    @app.route("/home" , methods=["GET"])
    def user_home():
        if "user_id" not in session:
            flash("Please log in to save exercises", "danger")
            return redirect(url_for("login"))
        # Sample classes data
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



    # Dashboard
    @app.route('/dashboard')
    def dashboard():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session['role'] != 'admin':
            flash("Access denied", "danger")
            return redirect(url_for('user_home'))
        users = User.query.all()
        return render_template('dashboard.html', users=users)

    # Logout
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('index'))

    # ------------------ EXERCISES ------------------

    EXERCISE_API_URL = "https://exercisedb-api1.p.rapidapi.com/api/v1"
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
                url = f"{EXERCISE_API_URL}/exercises/search?search={query}"
                response = requests.get(url, headers=EXERCISE_HEADERS)
                if response.status_code == 200:
                    if response.status_code == 200:
                        data = response.json()
                        exercise_list = data.get("data", [])

        return render_template("exercises.html", exercises=exercise_list, selected=selected)


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

        flash("Exercise saved to your plan!", "success")
        return redirect(url_for("exercises"))

    @app.route("/my_exercises")
    def my_exercises():
        if "user_id" not in session:
            return redirect(url_for("login"))

        saved_exercises = UserExercise.query.filter_by(user_id=session["user_id"]).all()
        return render_template("my_exercises.html", exercises=saved_exercises)

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

    return app


