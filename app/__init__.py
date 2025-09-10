from flask import Flask, render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get("SECRET_KEY", "super-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI",
        "sqlite:///shviki.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .models import User

    with app.app_context():
        db.create_all()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if request.method == 'POST':
            if User.query.filter_by(email=request.form['email']).first():
                flash("Email already registered", "danger")
                return redirect(url_for('register'))
            if User.query.filter_by(national_id=request.form['national_id']).first():
                flash("national_id already registered", "danger")
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
            return redirect(url_for('dashboard'))
        return render_template('register.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            user = User.query.filter_by(email=request.form['email']).first()
            if user and check_password_hash(user.password_hash, request.form['password']):
                session['user_id'] = user.id
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid email or password", "danger")
        return render_template('login.html')

    @app.route('/dashboard')
    def dashboard():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        users = User.query.all()
        return render_template('dashboard.html', users=users)

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('index'))

    return app
