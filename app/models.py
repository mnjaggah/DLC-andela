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
    is_learner = db.Column(db.Boolean, default=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'))
    my_courses = db.Column(db.PickleType)

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




class Target(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    is_done = db.Column(db.Boolean)
    task_name = db.Column(db.String(200), db.ForeignKey(
        'tasks.task_name'), nullable=False)

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    description = db.Column(db.String(200), unique=False)
    resource = db.Column(db.String(200), unique=False)
#tasks = db.relationship(Tasks, backref='courses', lazy='dynamic')

class Tasks(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(200), unique=True)
    task_description = db.Column(db.String(200), unique=False)
    target = db.relationship(Target, backref='tasks', lazy='dynamic')
    course_id = db.Column(db.Integer, db.ForeignKey(
        'courses.id'), nullable=False)
    course = db.relationship(Course, backref='course', lazy='dynamic')





