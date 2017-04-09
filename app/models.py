
from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app import login_manager


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


class User(db.Model):
    """The class User will be used to create a table that
    will store the information regarding the users"""
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = Column(String(20))
    lastname = Column(String(20))
    email = Column(String(120))
    password_hash = Column(db.String)
    role = Column(String(10))

    def __init__(self, email, firstname, lastname, password):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password_hash = generate_password_hash(password)
        self.role = "Learner"

    def check_password(self, password):
        """A method to be used to check if the password
        supplied matches with the encrypted password in the db"""
        return check_password_hash(self.password_hash, password)

    def make_facilitator(self):
        """A method that allows an admin to make a user
        as to be  afacilitator"""
        self.role = "Facilitator"

    def make_admin(self):
        """A method that allows an admin to allocate
        admin roles to a user"""
        self.role = "Admin"

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
