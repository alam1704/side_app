from main import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# Multiple inheritance from UserMixin provides useful instance methods such as :
    # is_authenticated() - checks if user is currently logged in
    # get_id() - looks up authenticated user in database. Allows us to retrieve their other information.
class User(UserMixin, db.Model):

    __tablename__ = 'flasklogin-users'
    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=False,
    )
    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )
    password = db.Column(
        db.String(200),
        nullable=False
    )

    is_admin = db.Column(
        db.Boolean(),
        server_default="0",
        nullable=True
    )
    # is_superadmin = db.Column(
    #     db.Boolean(),
    #     nullable=False,
    #     server_default="0"
    # )

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def image_filename(self):
        return f"user_images/{self.id}.png"

