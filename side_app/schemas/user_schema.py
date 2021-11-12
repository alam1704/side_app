from main import ma 
from models.users import User
from marshmallow_sqlalchemy import auto_field 
from marshmallow import fields, exceptions, validate
from werkzeug.security import generate_password_hash

# model: similar to our pharmacy model.
# email is getting validated to ensure it is in the right format.
# password: fields.method - gets it value based on a function rather than a dictionary input.
    # calls the 'load_password' function and performs validation and hashes the password.
    # the "load_only" argument ensures the data is never returned from the database - only writes TO the database. 
class UserSchema(ma.SQLAlchemyAutoSchema):
    id = auto_field(dump_only=True)
    name = auto_field(required=True, validate=validate.Length(min=1))
    email = auto_field(required=True, validate=validate.Email())
    password = fields.Method(
        required=True, 
        load_only=True, 
        deserialize="load_password"
    )
    
    def load_password(self, password):
        if len(password)>6:
            return generate_password_hash(password, method='sha256')
        raise exceptions.ValidationError("Password must be at least 6 characters.")
    
    # what is the Meta?
    class Meta:
        model = User
        load_instance = True

# schema objects: singular and plural schema similar to the pharmacy schema. 
# partial schema: won't throw an error if it doesn't receive a value for every field.
user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_update_schema = UserSchema(partial=True)