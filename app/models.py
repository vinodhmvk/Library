from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from app import db
from login import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from routes import login


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    books = db.relationship('Book', backref='lendee', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username) 
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Lender(db.Model):
    __tablename__ = "lenders"
 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return "<Lender: {}>".format(self.name)
 
 
class Book(db.Model):
    """"""
    __tablename__ = "books"
 
    id = db.Column(db.Integer, primary_key=True)
    lender = db.Column(db.Integer, db.ForeignKey('users.username') )
    book_name = db.Column(String)
    author = db.Column(String)
    genre = db.Column(String)
    summary = db.Column(String)

    """
    lender_id = db.Column(db.Integer, db.ForeignKey("lenders.id"))
    lender_name = db.relationship("Lender", backref=db.backref(
        "books", order_by=id), lazy=True)
    """
