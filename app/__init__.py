import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SECRET_KEY'] = 'D[\xa5E\x89\x01\xf9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Andela-DLC.db')
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.init_app(app)

import models
import views
