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


class ResourcesForm(FlaskForm):
    """ Form for admin to add resources link """
    url = URLField('URL', validators=[DataRequired()])
submit = SubmitField('Add')