import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SECRET_KEY'] = 'D[\xa5E\x89\x01\xf9'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'Andela-dlc.db')
app.config['DEBUG'] = True
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from . import models
from . import views


from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint)

from .facilitator import facilitator as facilitator_blueprint
app.register_blueprint(facilitator_blueprint, url_prefix='/facilitator')

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)