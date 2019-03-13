from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import logging
from logging.handlers import RotatingFileHandler
from flask_rq2 import RQ
from redis import Redis

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)
db = SQLAlchemy(app)  # The database object
migrate = Migrate(app, db)  # Used for database migrations to ensure db state
login = LoginManager(app)  # Used for logging into Truck-n-Load
login.login_view = 'login'  # Used to require users to be logged in to navigate to routes marked with `@login_required`
bootstrap = Bootstrap(app)  # Bootstrap for UI

# Logging
handler = RotatingFileHandler('logs/trucknload.log', maxBytes=10000, backupCount=3)
formatter = logging.Formatter("[%(asctime)s] [%(process)d] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# Delayed jobs
rq = RQ(app)
rq.init_app(app)

from app import routes, models
