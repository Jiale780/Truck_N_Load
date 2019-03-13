import os
from dotenv import load_dotenv
from pathlib import Path

# Loads the ./.env file into the system environment variables
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # The application is not required to be signaled on DB change
