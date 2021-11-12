from flask import Blueprint, request, render_template, redirect, url_for, abort, flash
from main import db, lm
from models.users import User
from schemas.user_schema import users_schema, user_schema, user_update_schema
from flask_login import login_user, logout_user, login_required, current_user
from marshmallow import ValidationError

# need to add some code that is unique to authentication controllers
# get user instance based on the session information in their browser cookie
# bouncing users who arent authorised - we are redirecting to the route for logging in.
@lm.user_loader
def load_user(user):
    return User.query.get(user)

@lm.unauthorized_handler
def unauthorized():
    return redirect('/users/login/')

# need a blueprint - just like pharmacy controller
users = Blueprint('users', __name__)

# create a route to display list of all users
@users.route("/users/", methods=["GET"])
def get_users():
    data = {
    "page_title": "User Index",
    "users": users_schema.dump(User.query.all())
    }
    return render_template("user_index.html", page_data = data)

# create a sign up route
# instead of separating GET and POST, we handle both in one route
    # If its a GET, we return the FORM page
    # If its a POST, we create user, log them in, then redirect them to the user index page.
@users.route("/users/signup/", methods = ["GET", "POST"])
def sign_up():
    data = {"page_title": "Sign Up"}
    
    if request.method == "GET":
        return render_template("signup.html", page_data = data)
    
    new_user = user_schema.load(request.form)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return redirect(url_for("users.get_users"))

# make a log in route
@users.route("/users/login/", methods=["GET", "POST"])
def log_in():
    data = {"page_title":"Log In"}

    if request.method == "GET":
        return render_template("login.html", page_data = data)

    user = User.query.filter_by(email=request.form["email"]).first()
    if user and user.check_password(password=request.form["password"]):
        login_user(user)
        return redirect(url_for('pharmacies.get_pharmacies'))

    abort(401, "Login Unsuccessful. Please enter valid username and password.")

# user details 
@users.route("/users/account/", methods=["GET", "POST"])
# to restrict a route to just users who are logged in:
# if they're not logged in they'll be redirected to the login page
@login_required

def user_detail():
    if request.method == "GET":
        data = {"page_title":"Account Details"}
        return render_template("user_detail.html", page_data = data)

    user = User.query.filter_by(id = current_user.id)
    updated_fields = user_schema.dump(request.form)
    # to check for errors
    errors = user_update_schema.validate(updated_fields)

    if errors:
        raise ValidationError(message=errors)

    user.update(updated_fields)
    db.session.commit()
    return redirect(url_for("users.get_users"))

# log out view
@users.route("/users/logout/", methods=["POST"])
@login_required
def log_out():
    logout_user()
    return redirect(url_for("users.log_in"))

