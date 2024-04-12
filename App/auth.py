from flask import Blueprint,request,render_template


auth = Blueprint('auth', __name__)


@auth.route("/login")
def login():
    return render_template('login.html')


@auth.route("/sign-up")
def sign_up():
    return "Sign up"


@auth.route("/logout")
def logout():
    return "logged out"

