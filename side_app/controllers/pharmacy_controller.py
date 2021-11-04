from flask import Blueprint, jsonify, request
from main import db
from models.pharmacy import Pharmacy

pharmacies = Blueprint('pharmacies', __name__)

# 'View' code
# 
# This one is just a placeholder for now, no CRUD here
@pharmacies.route('/')
def homepage():
    """
    The homepage route. 
    
    This will later contain information about what classes are available to enroll in.
    '/' is the address here, which means it will be available from our host domain. 
    During production this is localhost:5000 or 127.0.0.1:5000
    """
    return "Hello, world! Check this out!"

#db.create_all()
# create the table in our database to match our model
# This is the equivalent of the line from our Psycopg example code that began with CREATE TABLE IF NOT EXISTS... The difference here is that it will create as many tables as we need for the models we have, and it doesn't need to be told what SQL to use - it figures it out for itself!

@pharmacies.route("/pharmacies/", methods=["GET"])
def get_pharmacies():
    pharmacies = Pharmacy.query.all()
    return jsonify([pharmacy.serialize for pharmacy in pharmacies])

@pharmacies.route("/pharmacies/", methods = ["POST"])
def create_pharmacy():
    new_pharmacy = Pharmacy(request.json['pharmacy_name'])
    db.session.add(new_pharmacy)
    db.session.commit()
    return jsonify(new_pharmacy.serialize)

@pharmacies.route("/pharmacies/<int:id>/", methods = ["GET"])
def get_pharmacy(id):
    pharmacy = Pharmacy.query.get_or_404(id)
    return jsonify(pharmacy.serialize)

@pharmacies.route("/pharmacies/<int:id>/", methods=["PUT", "PATCH"])
def update_pharmacy(id):
    pharmacy = Pharmacy.query.filter_by(pharmacy_id=id)
    pharmacy.update(dict(pharmacy_name = request.json["pharmacy_name"]))
    db.session.commit()
    return jsonify(pharmacy.first().serialize)

@pharmacies.route("/pharmacies/<int:id>/", methods = ["DELETE"])
def delete_pharmacy(id):
    pharmacy = Pharmacy.query.get_or_404(id)
    db.session.delete(pharmacy)
    db.session.commit()
    return jsonify(pharmacy.serialize)