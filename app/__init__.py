from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_mail import Mail
from .util import filters

# Create Flask app instance
app = Flask(__name__)

# Set configurations from object defined in config.py
app.config.from_object(Config)
app.jinja_env.filters['nth'] = filters.nth
app.jinja_env.filters['to_date'] = filters.to_date

# Set database to app
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Login
login = LoginManager(app)
login.login_view = 'login'

# Email support
mail = Mail(app)

# Moment for date consistency
moment = Moment(app)

# Import modules
from app import routes, models, errors