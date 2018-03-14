from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from login import LoginForm

engine = create_engine('sqlite:///allbooks.db', echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username) 

class Lender(Base):
    __tablename__ = "lenders"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        """"""
        self.name = LoginForm().username

    def __repr__(self):
        return "<Lender: {}>".format(self.name)


class Book(Base):
    """"""
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    lender = Column(String)
    book_name = Column(String)
    author = Column(String)
    genre = Column(String)
    summary = Column(String)

    """
    lender_id = db.Column(db.Integer, db.ForeignKey("lenders.id"))
    lender_name = db.relationship("Lender", backref=db.backref(
        "books", order_by=id), lazy=True)
    """

    def __init__(self, lender, book_name, author, genre, summary):
        """"""
        self.lender = lender
        self.book_name = book_name
        self.author = author
        self.genre = genre
        self.summary = summary

# create tables
Base.metadata.create_all(engine)