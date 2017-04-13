from datetime import datetime
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app import login_manager


@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    target_id =db.Column(db.Integer, db.ForeignKey('target.id'))
    facilitator = db.Column(db.String(120), db.ForeignKey('facilitator.email'))
    my_courses = db.Column(db.PickleType)
    is_admin = db.Column(db.Boolean, default=False)
    is_learner = db.Column(db.Boolean, default=True)

    #task = db.relationship('Task', backref='task', lazy='dynamic')

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
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    description = db.Column(db.Text)
    user = db.relationship('User', backref='course',lazy='dynamic')
    tasks = db.relationship('Task', backref='course', lazy='dynamic')


class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    targets = db.relationship('Target', backref='task', lazy='dynamic')
    #user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref='task', lazy='dynamic')

class Target(db.Model):
    __tablename__ = 'target'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    is_done = db.Column(db.Boolean)
    task_id = db.Column(db.String, db.ForeignKey('task.id'))
    user = db.relationship('User', backref='target', lazy='dynamic')

class Facilitator(db.Model, UserMixin):
    __tablename__ = 'facilitator'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), unique=False)
    last_name = db.Column(db.String(64), unique=False)
    email = db.Column(db.String(120), unique=True)
    learner = db.relationship('User', backref='facilitators', lazy='dynamic')    

"""class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    user = db.relationship('User',backref=db.backref('comments', lazy='dynamic'))
    task = db.relationship('Task', backref=db.backref('comments', lazy='dynamic'))   """