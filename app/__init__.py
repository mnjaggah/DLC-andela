import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)

# Need to set secret key for creating secure cookies
app.config['SECRET_KEY'] = 'D[\xa5E\x89\x01\xf9'
# setup database connection and uri
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Andela-DLC.db')
app.config['DEBUG'] = True
# intialize sqlalchemy by calling the sqlalchemy constructor
db = SQLAlchemy(app)

#configure authentication
login_manager = LoginManager()
login_manager.session_protection = 'strong'
# if user is anonymous redirect to login page
login_manager.login_view = 'login'
login_manager.init_app(app)

import models
import views
