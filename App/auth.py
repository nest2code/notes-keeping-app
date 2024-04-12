from flask import Blueprint, request, redirect, url_for, render_template, flash
from .models import User, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password1 = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password1):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Invalid password', category='error')
        else:
            flash('invalid email', category='success')
    return render_template('login.html',user = current_user)


@auth.route("/sign-up", methods=['POST', "GET"])
def sign_up():
    if request.method == "POST":
        email = request.form.get('email')
        user_name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        print(user_name, email)
        print(password1, password2)
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email exists', category='error')
        elif len(user_name) < 4:
            flash('Invalid Username', category='error')
        elif password1 != password2:
            flash('Password not match', category='error')
        else:
            flash('Account created', category='success')
            new_user = User(email=email, name=user_name,
                            password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('auth.login'))
    return render_template('register.html',user = current_user)


@auth.route("/logout")
@login_required
def logout():
    return redirect('auth.login')
