import unittest
import os

from flask import Flask
from flask_testing import TestCase
from flask import url_for
from flask.ext.sqlalchemy import SQLAlchemy

from app import db
from app.models import Course


class TestBase(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True
    db = SQLAlchemy()

    def create_app():
        app = Flask(__name__)
        db.init_app(app)
        with app.app_context():
            db.create_all()
        return app

    def setUp(self):
        db.create_all()
        admin = User(username='admin',
                     email='admin@andela.com', password='andela')
        db.session.add(admin)
        db.session.add(employee)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TestModels(TestBase):
    def test_course_model(self):
        """ Test number of records in Course table """
        course = Course(
            name="Amity", description="Allocates offices and rooms randomly")
        db.session.add(course)
        db.session.commit()

        self.assertEqual(Course.query.count(), 1)


class TestViews(TestBase):

    def test_dashboard_view(self):
        """ Test that admin dashboard is accessible without login """
        target_url = url_for('dashboard')
        redirect_url = url_for('auth.login', next=target_url)
        response = self.client.get(target_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)


if __name__ == '__main__':
    unittest.main()
