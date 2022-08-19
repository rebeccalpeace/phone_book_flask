from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

# create an instance of SQLAlchemy (the ORM) with the Flask Application
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

from . import routes, models

