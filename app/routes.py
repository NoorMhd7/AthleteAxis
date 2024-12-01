from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .models import User
from .forms import RegistrationForm, LoginForm

main = Blueprint('main', __name__)

# Index Route (Home Page)
@main.route('/')
def index():
    print("Reached index route")
    return render_template('base.html')

# Shop Page Route
@main.route('/shop')
def shop():
    return 'Shop Page'

# About Page Route
@main.route('/about')
def about():
    return 'About Page'

# Contact Page Route
@main.route('/contact')
def contact():
    return 'Contact Page'

# Cart Page Route
@main.route('/cart')
def cart():
    return 'Cart Page'

# Registration Route
@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('main.index'))  # Redirect to the home page after successful registration
    return render_template('register.html', title='Register', form=form)

# Login Route
@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))  # Redirect to the home page if already logged in

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            return redirect(url_for('main.index'))  # Redirect to the home page after successful login
    return render_template('login.html', title='Login', form=form)

# Logout Route
@main.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.index'))  # Redirect to home page after logout

@main.route("/profile")
@login_required
def profile():
    return render_template('profile.html', title='Profile')
