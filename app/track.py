
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()
engine = create_engine("sqlite:///Andela-dlc.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class Challenge(Base):
    """The class Card will be used to create a table that
    will store the information regarding the Challenges"""
    __tablename__ = "Challenge"
    challenge_id = Column(Integer, primary_key=True, autoincrement=True)
    board_name = Column(String(50))
    skill_name = Column(String(50))
    challenge_name = Column(String(50))
    status = Column(String(10))

    def __init__(self, board_name, skill_name, challenge_name):
        self.board_name = board_name
        self.skill_name = skill_name
        self.challenge_name = challenge_name
        self.status = "To-Do"
    
    def change_to_doing(self):
        self.status = "Doing"
    
    def change_to_done(self):
        self.status = "Done"
    
    def archive(self):
        self.status = None

class Skill(Base):
    """The class Card will be used to create a table that
    will store the information regarding the Card"""
    __tablename__ = "cards"
    board_name = Column(String(50))
    name = Column(String(50), primary_key=True, autoincrement=False)
    status = Column(String(10))
    
    def __init__(self, board_name, name):
        self.board_name = board_name
        self.name = name
        self.status = "To-Do"
    
    def add_challenge(self, challenge_name):
        new_challenge = Challenge(self.board_name, self.skill_name, challenge_name)
        session.add(new_challenge)
        session.comit()
        return new_challenge
    
    def change_to_doing(self):
        self.status = "Doing"
    
    def change_to_done(self):
        self.status = "Done"
    
    def archive(self):
        self.status = None

class Board(Base):
    """The class Board will be used to create a table that
    will store the information regarding the boards"""
    __tablename__ = "boards"
    board_id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(50), unique=True)
    
    def __init__(self, name):
        self.name = name
    
    def add_skill(self, card_name):
        new_card = Skill(self.name, card_name)
        session.add(new_card)
        session.comit()
        return new_skill

Base.metadata.create_all(engine)


