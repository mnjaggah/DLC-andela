from flask import Blueprint

facilitator = Blueprint('facilitator', __name__)

from . import views