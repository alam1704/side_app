from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from main import db
from models.pharmacy import Pharmacy
from schemas.pharmacy_schema import pharmacies_schema, pharmacy_schema

# this is a controller in the ModelViewsController model.
pharmacies = Blueprint('pharmacies', __name__)

# 'View' code
# This one is just a placeholder for now, no CRUD here
@pharmacies.route('/')
def homepage():
    data = {
        "page_title" : "Home Page"
    }
    return render_template("homepage.html", page_data = data)

#db.create_all()
# create the table in our database to match our model
# This is the equivalent of the line from our Psycopg example code that began with CREATE TABLE IF NOT EXISTS... The difference here is that it will create as many tables as we need for the models we have, and it doesn't need to be told what SQL to use - it figures it out for itself!

@pharmacies.route("/pharmacies/", methods=["GET"])
def get_pharmacies():
    pharmacies = Pharmacy.query.all()
    data = {
        "page_title" : "Pharmacy Index",
        "pharmacies" : pharmacies_schema.dump(pharmacies)
    }
    return render_template("pharmacy_index.html", page_data = data)

@pharmacies.route("/pharmacies/", methods = ["POST"])
def create_pharmacy():
    new_pharmacy = pharmacy_schema.load(request.form)
    db.session.add(new_pharmacy)
    db.session.commit()
    return redirect(url_for("pharmacies.get_pharmacies"))

@pharmacies.route("/pharmacies/<int:id>/", methods = ["GET"])
def get_pharmacy(id):
    pharmacy = Pharmacy.query.get_or_404(id)
    data = {
        "page_title" : "Pharmacy Detail",
        "pharmacy" : pharmacy_schema.dump(pharmacy)
    }
    return render_template("pharmacy_detail.html", page_data = data)

@pharmacies.route("/pharmacies/<int:id>/", methods=["POST"])
# import login_required decorator then put log_in decorator
def update_pharmacy(id):
    pharmacy = Pharmacy.query.filter_by(pharmacy_id=id)
    updated_fields = pharmacy_schema.dump(request.form)
    if updated_fields:
        pharmacy.update(updated_fields)
        db.session.commit()
    data = {
        "page_title" : "Pharmacy Detail",
        "pharmacy" : pharmacy_schema.dump(pharmacy.first())
    }
    return render_template("pharmacy_detail.html", page_data = data)

@pharmacies.route("/pharmacies/<int:id>/delete/", methods = ["POST"])
def delete_pharmacy(id):
    pharmacy = Pharmacy.query.get_or_404(id)
    db.session.delete(pharmacy)
    db.session.commit()
    return redirect(url_for("pharmacies.get_pharmacies"))