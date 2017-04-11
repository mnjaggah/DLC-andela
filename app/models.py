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
    questions = db.relationship('ForumQuestion', backref='user', lazy='dynamic')
    answers = db.relationship('ForumAnswer', backref='user', lazy='dynamic')
    replies = db.relationship('ForumAnswerReply', backref='user', lazy='dynamic')
    question_votes = db.relationship('QuestionVotes', backref='user', lazy='dynamic')
    answer_votes = db.relationship('AnswerVotes', backref='user', lazy='dynamic')

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


class ForumQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    forum_category = db.Column(db.String(80))
    forum_title = db.Column(db.String(80))
    forum_question = db.Column(db.Text(80))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    question_owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    answers = db.relationship('ForumAnswer', backref='forum_question', lazy='dynamic')
    question_votes = db.relationship('QuestionVotes', backref='forum_question', lazy='dynamic')

    def __repr__(self):
        return "<Questions '{}'>".format(self.forum_question)


class ForumAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    forum_answer = db.Column(db.String(80))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    best_answer = db.Column(db.Boolean, default=False)
    answer_owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    answer_question_id = db.Column(db.Integer, db.ForeignKey('forum_question.id'), nullable=False)
    replies = db.relationship('ForumAnswerReply', backref='forum_answer', lazy='dynamic')
    answer_votes = db.relationship('AnswerVotes', backref='forum_answer', lazy='dynamic')


class ForumAnswerReply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reply_text = db.Column(db.String(80))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    reply_owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reply_answer_id = db.Column(db.Integer, db.ForeignKey('forum_answer.id'), nullable=False)


class QuestionVotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vote_owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('forum_question.id'), nullable=False)
    is_upvote = db.Column(db.Boolean, default=False)
    is_downvote = db.Column(db.Boolean, default=False)


class AnswerVotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vote_owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    answer_id = db.Column(db.Integer, db.ForeignKey('forum_answer.id'), nullable=False)
    is_upvote = db.Column(db.Boolean, default=False)
    is_downvote = db.Column(db.Boolean, default=False)
