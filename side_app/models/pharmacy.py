from main import db

# It might not look like much, but this db object is going to do all the work of communicating with our database for us, generating all the SQL we need!
# Our first model! 
# This tells the ORM what tables should exist in the database
# It also lets us retrieve info from those tables
class Pharmacy(db.Model):
    # The tablename attribute specifies what the name of the table should be
    __tablename__ = "pharmacies"

    # These attributes specify what columns the table should have
    pharmacy_id = db.Column(db.Integer, primary_key=True)
    pharmacy_name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), default="No description provided...")
    phone_number = db.Column(db.Integer, nullable=False, default=0)


