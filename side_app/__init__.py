import os
from flask import Flask, json, jsonify, request
from flask_sqlalchemy import SQLAlchemy

(
    db_user, 
    db_pass, 
    db_name, 
    db_domain
) = (os.environ.get(item) for item in [
    "DB_USER", 
    "DB_PASS", 
    "DB_NAME", 
    "DB_DOMAIN"
    ]
)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_domain}/{db_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#This is going to let SQLAlchemy figure out how to connect to connect to the database, and also silence some pesky warnings.

db = SQLAlchemy(app)

# It might not look like much, but this db object is going to do all the work of communicating with our database for us, generating all the SQL we need!

class Pharmacy(db.Model):
    __tablename__ = "pharmacies"
    pharmacy_id = db.Column(db.Integer, primary_key=True)
    pharmacy_name = db.Column(db.String(80), unique=True, nullable=False)

    # creates table with the specified columns, also allows us to get information from the table
    
    def __init__(self, pharmacy_name):
        self.pharmacy_name = pharmacy_name

    # Note we do not initialise a pharmacy_id because we are using the flask app to do this.

    @property
    def serialize(self):
        return {
            "pharmacy_id": self.pharmacy_id,
            "pharmacy_name": self.pharmacy_name
        }

    # We also have a property called serialize in there! We will end up replacing it, but for now this is responsible for turning our model into a dictionary, so that it can be converted into JSON.

db.create_all()
# create the table in our database to match our model
# This is the equivalent of the line from our Psycopg example code that began with CREATE TABLE IF NOT EXISTS... The difference here is that it will create as many tables as we need for the models we have, and it doesn't need to be told what SQL to use - it figures it out for itself!

@app.route("/pharmacies/", methods=["GET"])
def get_pharmacies():
    pharmacies = Pharmacy.query.all()
    return jsonify([pharmacy.serialize for pharmacy in pharmacies])

@app.route("/pharmacies/", methods = ["POST"])
def create_pharmacy():
    new_pharmacy = Pharmacy(request.json['pharmacy_name'])
    db.session.add(new_pharmacy)
    db.session.commit()
    return jsonify(new_pharmacy.serialize)

@app.route("/pharmacies/<int:id>/", methods = ["GET"])
def get_pharmacy(id):
    pharmacy = Pharmacy.query.get_or_404(id)
    return jsonify(pharmacy.serialize)

@app.route("/pharmacies/<int:id>/", methods=["PUT", "PATCH"])
def update_pharmacy(id):
    pharmacy = Pharmacy.query.filter_by(pharmacy_id=id)
    pharmacy.update(dict(pharmacy_name = request.json["pharmacy_name"]))
    db.session.commit()
    return jsonify(pharmacy.first().serialize)

@app.route("/pharmacies/<int:id>/", methods = ["DELETE"])
def delete_pharmacy(id):
    pharmacy = Pharmacy.query.get_or_404(id)
    db.session.delete(pharmacy)
    db.session.commit()
    return jsonify(pharmacy.serialize)


# @app.route('/')
# def hello_world():
#     """
#     The homepage route. 
    
#     This will later contain information about what classes are available to enroll in.
#     '/' is the address here, which means it will be available from our host domain. 
#     During production this is localhost:5000 or 127.0.0.1:5000
#     """
#     return "Hello, world! Check this out!"
    
if __name__ == '__main__':
    app.run(debug=True)