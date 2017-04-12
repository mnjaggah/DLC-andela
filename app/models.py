from datetime import datetime
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app import login_manager


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String)
    is_admin = db.Column(db.Boolean, default=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    is_learner = db.Column(db.Boolean, default=True)
    facilitator = db.Column(db.String(120), db.ForeignKey('facilitator.email'))
    my_courses = db.Column(db.PickleType)
    task = db.relationship('Task', backref='task', lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    def __repr__(self):
        return "<User '{}'>".format(self.username)


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.Text)
    learners = db.relationship('User', lazy='dynamic')
    tasks = db.relationship('Task', backref='course', lazy='dynamic')


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    targets = db.relationship('Target', backref='task', lazy='dynamic')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Target(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    is_done = db.Column(db.Boolean)
    task_id = db.Column(db.String, db.ForeignKey('task.id'))


class Facilitator(db.Model, UserMixin):
    __tablename__ = 'facilitator'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), unique=False)
    last_name = db.Column(db.String(64), unique=False)
    email = db.Column(db.String(120), unique=True)
    learner = db.relationship('User', backref='facilitators', lazy='dynamic')    