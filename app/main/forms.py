from flask_wtf import Form, FlaskForm
from wtforms.fields import StringField, PasswordField, BooleanField, SubmitField, TextField
from wtforms.validators import DataRequired, url, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from wtforms.fields.html5 import URLField
from ..models import User


class CoursesForm(FlaskForm):
    """ Form for admin to add or edit a course """
    name = StringField('Course Name', validators=[DataRequired()])
    description = TextField(
        'Description', validators=[DataRequired()])
    submit = SubmitField('Create')


class TasksForm(FlaskForm):
    """ Form for admin to add course tasks"""
    TaskName = StringField('TaskName', validators=[DataRequired()])
    description = TextField(
        'Description', validators=[DataRequired()])
    submit = SubmitField('Add task')

class AddFacilitatorsForm(Form):
    """
    Form to add facilitators to system
    """

    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Save')
    

class FacilitatorLoginForm(Form):

    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Login')
