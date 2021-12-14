from marshmallow import Schema, fields

from pprint import pprint

import datetime as dt


class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.created_at = dt.datetime.now()

    def __repr__(self):
        return "<User(name={self.name!r})>".format(self=self)

class UserSchema(Schema):
    name = fields.Str()
    email = fields.Email()
    created_at = fields.Date()

user = User(name="Monty", email="monty@python.org")
schema = UserSchema()
result = schema.dump(user)
pprint(result)