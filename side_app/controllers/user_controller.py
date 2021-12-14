from flask import Blueprint, request, render_template, redirect, url_for, abort, flash, current_app
from main import db, lm
from models.users import User
from models.pharmacy import Pharmacy
from schemas.user_schema import users_schema, user_schema, user_update_schema
from schemas.pharmacy_schema import pharmacies_schema, pharmacy_schema
from flask_login import login_user, logout_user, login_required, current_user
from marshmallow import ValidationError
import boto3

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

@users.route("/")
def home():
    data = {
        "page_title": "Home"
    }
    return render_template("index.html", page_data=data)

# create a sign up route
# instead of separating GET and POST, we handle both in one route
    # If its a GET, we return the FORM page
    # If its a POST, we create user, log them in, then redirect them to the user index page.
@users.route("/users/signup/", methods = ["GET", "POST"])
def sign_up():
    """Displayes the signup form and creates new user when the form is submitted"""
    data = {"page_title": "Sign Up"}
    
    if request.method == "GET":
        return render_template("signup.html", page_data = data)
    else:

        new_user = user_schema.load(request.form)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("users.get_user", id=new_user.id))

# make a log in route
@users.route("/users/login/", methods=["GET", "POST"])
def log_in():
    data = {
        "page_title":"Log In"
        }

    if request.method == "GET":
        return render_template("login.html", page_data = data)
    else:
        user = User.query.filter_by(email=request.form["email"]).first()
        if user and user.check_password(password=request.form["password"]):
            login_user(user)
            return redirect(url_for('pharmacies.get_pharmacies'))
        else:
            abort(401, "Login Unsuccessful. Please enter valid username and password.")

# log out view
@users.route("/users/logout/", methods=["POST"])
@login_required
def log_out():
    logout_user()
    return redirect(url_for("users.log_in"))

@users.route("/users/", methods=["GET"])
def get_users():
    """Create a route to display list of all users from the database"""
    users=User.query.all()
    data = {
        "page_title": "All Users",
        "users": users_schema.dump(users)
    }
    return render_template("user_index.html", page_data = data)


# user details 
@users.route("/users/account/", methods=["GET", "POST"])
# to restrict a route to just users who are logged in:
# if they're not logged in they'll be redirected to the login page
@login_required
def edit_user():
    if request.method == "GET":
        data = {"page_title":"Edit Account Details"}
        return render_template("user_detail.html", page_data = data)
    else:
        user = User.query.filter_by(id = current_user.id)
        updated_fields = user_update_schema.dump(request.form)
        # to check for errors
        errors = user_update_schema.validate(updated_fields)

        if errors:
            raise ValidationError(message=errors)

        user.update(updated_fields)
        db.session.commit()
        return redirect(url_for("users.get_users", id=current_user.id))



# An endpoint to GET info about a specific course
@users.route("/user/<int:id>", methods = ["GET"])
@login_required
def get_user(id):
    user = User.query.get_or_404(current_user.id)
    pharmacies = Pharmacy.query.where(Pharmacy.pharmacy_id == current_user.id)
    
    s3_client=boto3.client("s3")
    bucket_name=current_app.config["AWS_S3_BUCKET"]
    image_url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            "Bucket": bucket_name,
            "Key": f"user_images/{user.image_filename}"
        },
        ExpiresIn=3600*24
    )
    
    data = {
        "page_title": user.name,
        "user": user_schema.dump(user),
        "pharmacies": pharmacies_schema.dump(pharmacies),
        "image": image_url
    }
    return render_template("user_detail.html", page_data=data)


