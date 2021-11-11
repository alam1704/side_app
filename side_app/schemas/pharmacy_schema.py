from main import ma
from models.pharmacy import Pharmacy

# lets marshmallow take a look at our model and create a field conversion function.
# figures out to turn json --> model and model --> json
from marshmallow_sqlalchemy import auto_field

from marshmallow.validate import Length

# using the ma object to create a schema.
class PharmacySchema(ma.SQLAlchemyAutoSchema):
    # this is the equivalent of saying "you should only expect to get a value for pharmacy_id when the information is coming from the database.
    # the auto field infers that the input has to be a string - validation tests
    # Likewise with pharmacy name, length of name is validated with min char length of 1.
    pharmacy_id = auto_field(dump_only=True)
    pharmacy_name = auto_field(required=True, validate=Length(min=1))


    # A schema for the Course model
    # Using it to load in information from a JSON and turn that into a Course instance
    # Equivalent to saying "Hey, in addition to all the facts about you as a class that Marshmallow is recording for us, you should know that you are a class that represents a model"
    class Meta:
        model = Pharmacy
        load_instance = True

pharmacy_schema = PharmacySchema()
pharmacies_schema = PharmacySchema(many=True)