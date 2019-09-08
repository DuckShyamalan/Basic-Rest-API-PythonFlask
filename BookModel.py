from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json

from sqlalchemy.orm import defer, session

from settings import app

db = SQLAlchemy(app)


class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    author = db.Column(db.String(80), nullable=False)
    isbn = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)

    #isDeleted = db.Column(db.Boolean(), default=False)

    def json(self):
        return {"title": self.title, "author": self.author, "isbn": self.isbn, "year": self.year}

    def addBook(_title, _author, _isbn, _year):
        new_book = Book(title=_title, author=_author, isbn=_isbn, year=_year)
        db.session.add(new_book)
        db.session.commit()

    def getAllBooks():
        return [Book.json(book) for book in Book.query.all()]
        #return [Book.json(book) for book in Book.query.options(defer(Book.is_deleted))]

    def getBook(_isbn):
        return Book.json(Book.query.filter_by(isbn=_isbn).first())

    def deleteBook(_isbn): # soft delete (do we just not use this and make it "delete" from app itself?)
        #bookToDelete = Book.query.filter_by(isbn=_isbn).first()
        #if not bookToDelete.isDeleted:
        #bookToDelete.isDeleted = True
        #db.session.commit()
        #return bookToDelete

        is_successful = Book.query.filter_by(isbn=_isbn).delete()
        db.session.commit()
        return bool(is_successful)

    def updateBookTitle(_isbn, _title):
        book_to_update = Book.query.filter_by(isbn=_isbn).first()
        book_to_update.title = _title
        db.session.commit()
        return book_to_update

    def updateBookAuthor(_isbn, _author):
        book_to_update = Book.query.filter_by(isbn=_isbn).first()
        book_to_update.author = _author
        db.session.commit()
        return book_to_update

    def updateBookYear(_isbn, _year):
        book_to_update = Book.query.filter_by(isbn=_isbn).first()
        book_to_update.year = _year
        db.session.commit()
        return book_to_update

    def replaceBook(_title, _author, _isbn, _year):
        book_to_replace = Book.query.filter_by(isbn=_isbn).first()
        book_to_replace.title = _title
        book_to_replace.author = _author
        book_to_replace.year = _year
        db.session.commit()
        return book_to_replace

    def __repr__(self):
        book_object = {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "year": self.year
        }
        return json.dumps(book_object)
