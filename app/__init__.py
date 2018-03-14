from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
#app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///allbooks.db'
app.secret_key = "flask rocks!"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models



