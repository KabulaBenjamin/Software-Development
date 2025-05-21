import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# Load environment variables from .env
load_dotenv()

from config import Config
from models import db, User  # Import the database instance and User model
from routes.members import members_bp
from routes.subscribers import subscribers_bp

app = Flask(__name__)
app.config.from_object(Config)

# Configure file upload folder for profile pictures
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"  # If unauthorized, redirect to login page
bcrypt = Bcrypt(app)


# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


# Register blueprints if any modular routes exist.
app.register_blueprint(members_bp, url_prefix="/members")
app.register_blueprint(subscribers_bp, url_prefix="/subscribers")


# Home route: Redirect authenticated users to the dashboard.
@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html', title="Home Page")


# Login route.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user, remember=remember)
            flash("Logged in successfully.", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials.", "danger")
    return render_template('login.html', title="Login")


# Signup route.
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password')
        confirm = request.form.get('confirm')

        if not username or not email or not password:
            flash("Please fill out all fields.", "danger")
            return render_template('signup.html', title="Sign Up")

        if password != confirm:
            flash("Passwords do not match.", "danger")
            return render_template('signup.html', title="Sign Up")

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("A user with that username or email already exists.", "danger")
            return render_template('signup.html', title="Sign Up")

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Signup successful! You can now log in.", "success")
        return redirect(url_for('login'))

    return render_template('signup.html', title="Sign Up")


# Profile route.
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == "POST":
        current_user.username = request.form.get("username")
        current_user.email = request.form.get("email")
        current_user.bio = request.form.get("bio")
        current_user.gender = request.form.get("gender")

        age = request.form.get("age")
        if age and age.isdigit():
            current_user.age = int(age)

        current_user.location = request.form.get("location")

        new_password = request.form.get("password")
        if new_password:
            current_user.password = bcrypt.generate_password_hash(new_password).decode("utf-8")

        file = request.files.get("profile_picture")
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            current_user.profile_picture = filename

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template("profile.html", user=current_user, title="Edit Profile")


# Dashboard route with role-based content.
@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'member':
        additional_content = "Welcome, esteemed member! Enjoy your exclusive benefits."
    elif current_user.role == 'subscriber':
        additional_content = "Hello subscriber! Check out the latest content available."
    else:
        additional_content = "Hello! Welcome to your dashboard."

    other_users = User.query.filter(User.id != current_user.id).all()
    return render_template("dashboard.html",
                           user=current_user,
                           users=other_users,
                           additional_content=additional_content,
                           title="Dashboard")


# Logout route.
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for('home'))


# Error handlers.
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(debug=True)