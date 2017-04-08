
from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()
engine = create_engine("sqlite:///Andela-DLC.db")
Base.metadata.bind = engine

class User(Base):
    """The class User will be used to create a table that
    will store the information regarding the users"""
    __tablename__ = "users"
    email = Column(String(50), primary_key=True, autoincrement=False)
    firstname = Column(String(20))
    surname = Column(String(20))
    pwdhash = Column(String(20))
    role = Column(String(10))

    def __init__(self, email, firstname, surname, password):
        self.email = email
        self.firstname = firstname
        self.surname = surname
        self.pwdhash = generate_password_hash(password)
        self.role = "Learner"

    def check_password(self, password):
        """A method to be used to check if the password
        supplied matches with the encrypted password in the db"""
        return check_password_hash(self.pwdhash, password)

    def make_facilitator(self):
        """A method that allows an admin to make a user
        as to be  afacilitator"""
        self.role = "Facilitator"
    
    def make_admin(self):
        """A method that allows an admin to allocate
        admin roles to a user"""
        self.role = "Admin"

Base.metadata.create_all(engine)


