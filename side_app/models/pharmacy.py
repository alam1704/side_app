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

    # The init method lets us create a python object to insert as a new row
    def __init__(self, pharmacy_name):
        self.pharmacy_name = pharmacy_name

    # Note we do not initialise a pharmacy_id because we are using the flask app to do this.
    # The serialize property lets us turn our course objects into JSON easily
    @property
    def serialize(self):
        return {
            "pharmacy_id": self.pharmacy_id,
            "pharmacy_name": self.pharmacy_name
        }

    # We also have a property called serialize in there! We will end up replacing it, but for now this is responsible for turning our model into a dictionary, so that it can be converted into JSON.