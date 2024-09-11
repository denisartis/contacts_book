from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask import Flask
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///contacts.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    group_name = db.Column(db.String(100), nullable=False)

