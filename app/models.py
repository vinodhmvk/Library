from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from app import db
from login import LoginForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from routes import login
from datetime import datetime

"""
Book_History = db.Table("book_history",
            db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
            db.Column('book_name', db.Integer, db.ForeignKey('books.book_name')),
            db.Column('borrower', db.Integer, db.ForeignKey('users.username')),
            db.Column('status', db.String(140)),
            db.Column('borrow_time', db.DateTime, index=True, default=datetime.utcnow))
"""
class Book_History(db.Model):
    """"""
    __tablename__ = "book_history"
 
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    book_name = db.Column(db.Integer, db.ForeignKey('books.book_name'))
    borrower = db.Column(db.Integer, db.ForeignKey('users.username') )
    status = db.Column(db.String(140))
    borrow_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    books = db.relationship('Book', backref='lendee', lazy='dynamic')
    books_his = db.relationship('Book_History', backref='borrowee', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username) 
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Book(db.Model):
    """"""
    __tablename__ = "books"
 
    id = db.Column(db.Integer, primary_key=True)
    lender = db.Column(db.Integer, db.ForeignKey('users.username') )
    book_name = db.Column(db.String(140))
    author = db.Column(db.String(140))
    genre = db.Column(db.String(140))
    summary = db.Column(db.String(140))
    current_status = db.Column(db.String(140))
    status = db.relationship(
        'Book', secondary=Book_History.__table__,
        primaryjoin=(Book_History.book_id == id),
        secondaryjoin=(Book_History.book_name == book_name),
        backref=db.backref('Book_History', lazy='dynamic'), lazy='dynamic')

    """
    lender_id = db.Column(db.Integer, db.ForeignKey("lenders.id"))
    lender_name = db.relationship("Lender", backref=db.backref(
        "books", order_by=id), lazy=True)
    """