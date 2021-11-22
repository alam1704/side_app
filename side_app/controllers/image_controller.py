from flask import Blueprint, request, redirect, abort, url_for, current_app
from pathlib import Path
from models.users import User
# S3 from our Flask application we will be using the AWS SDK boto3
# It is a library that gives us classes and functions to help make our lives easier when we are developing
import boto3

user_images = Blueprint('user_images', __name__)

@user_images.route("/users/<int:id>/image/", methods=["POST"])
def update_image(id):
    user=User.query.get_or_404(id)
    if "image" in request.files:
        image = request.files["image"]
        if Path(image.filename).suffix == ".png":
            bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
            bucket.upload_fileobj(image, f"{user.image_filename}.png")
        elif Path(image.filename).suffix == ".jpg":
            bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
            bucket.upload_fileobj(image, f"{user.image_filename}.jpg")
        elif Path(image.filename).suffix == ".pdf":
            bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
            bucket.upload_fileobj(image, f"{user.image_filename}.pdf")
        else:
            return abort(400, description="Invalid file type")
        
        # bucket = boto3.resource("s3").Bucket(current_app.config["AWS_S3_BUCKET"])
        # bucket.upload_fileobj(image, user.image_filename)

        

        # note that we have removed this line:
        # image.save(f"static/{course.image_filename}")
        
        return redirect(url_for("users.get_user", id=id))
    return abort(400, description="No image")