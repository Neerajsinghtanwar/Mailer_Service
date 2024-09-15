from app.app import app
import os
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS


DATABASE_PATH = os.path.join(os.path.abspath(os.getcwd()), 'test.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mypostgresdb:ooo1ooo1@localhost/mypostgresdb'

db = SQLAlchemy(app)

from app.models import *

with app.app_context():
    db.create_all()


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'example@gmail.com'
app.config['MAIL_PASSWORD'] = 'password'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

CORS(app, resources={r"/*": {"origins": "*"}})
