from flask import Flask, json, jsonify, request
from flask_sqlalchemy import SQLAlchemy

#This is going to let SQLAlchemy figure out how to connect to connect to the database, and also silence some pesky warnings.
db = SQLAlchemy()

def create_app():

    # using a list comprehension and multiple assignment 
    # to grab the environment variables we need

    # Creating the flask app object - this is the core of our app!
    app = Flask(__name__)

    #configuring our app
    app.config.from_object("config.app_config")

    #we are creating a generic db object that we can import into our models code, and then waiting until the create_app function is called to associate that db object with our app. Tricky!
    db.init_app(app)

    #register our routes
    from controllers import registerable_controllers
    for controller in registerable_controllers:
        app.register_blueprint(controller)
    
    return app

