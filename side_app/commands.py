# Creating custom command line interface commands for Flask
from main import db
from flask import Blueprint

# creating a blueprint to avoid passing around the app variable when we decorate a function
db_commands = Blueprint("db", __name__)

# command to create tables using SQLAlchemy with our registered models on the db variable.
@db_commands.cli.command("create")
def create_db():
    # the create all function
    db.create_all()
    print ("Tables created!")

# command to delete table using SQLAlchemy with our registered models on the db variable.
@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables deleted")

