import datetime

from flask import Flask, jsonify, request, Response
import json
from BookModel import *
from settings import *
import jwt
from UserModel import User
from functools import wraps


app.config["SECRET_KEY"] = "secret"


@app.route("/login", methods=["POST"])
def get_token():
    request_data = request.get_json()
    username = str(request_data["username"])
    password = str(request_data["password"])
    match = User.usernamePasswordMatch(username, password)
    if match:
        expiration_date = datetime.datetime.utcnow() + datetime.timedelta(seconds=100)
        token = jwt.encode({"exp": expiration_date}, app.config["SECRET_KEY"], algorithm="HS256")
        return token
    else:
        return Response("", 401, mimetype="application/json")


def validBookObject(bookObject):
    if "title" in bookObject and "author" in bookObject and "isbn" in bookObject and "year" in bookObject:
        return True
    else:
        return False


def validPutRequest(bookObject):
    if "title" in bookObject and "author" in bookObject and "year" in bookObject:
        return True
    else:
        return False


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get("token")
        try:
            jwt.decode(token, app.config["SECRET_KEY"])
            return f(*args, **kwargs)
        except:
            return jsonify({"error": "Need a valid token to access this page"}), 401
    return wrapper


@app.route("/books")
def getBooks():
    return jsonify({"books": Book.getAllBooks()})


@app.route("/books", methods=["POST"])
@token_required  # uses above token_required() method
def addBook():
    request_data = request.get_json()
    if validBookObject(request_data):
        Book.addBook(request_data["title"], request_data["author"], request_data["isbn"], request_data["year"])
        response = Response("", status=201, mimetype="application/json")
        response.headers["Location"] = "/books/" + str(request_data["isbn"])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book object passed in request",
            "helpString": "Pass an album object request in the form: {'title':'bookTitle', 'author':bookAuthor, "
                          "'isbn': isbn, 'year': year}"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), status=400, mimetype="application/json")
        return response


@app.route("/books/<int:isbn>")
def getBookByISBN(isbn):
    return_value = Book.getBook(isbn)
    return jsonify(return_value)


@app.route("/books/<int:isbn>", methods=["PUT"])
@token_required
def replaceBook(isbn):
    request_data = request.get_json()
    if not validPutRequest(request_data):
        invalidPutReqErrorMsg = {
            "error": "Invalid book object passed",
            "helpString": "Book should be passed as {'title', 'author', 'year'}"
        }
        response = Response(json.dumps(invalidPutReqErrorMsg), status=400, mimetype="application/json")
        return response
    Book.replaceBook(request_data["title"], request_data["author"], isbn, request_data["year"])
    response = Response("", status=204)
    return response


@app.route("/books/<int:isbn>", methods=["PATCH"])
@token_required
def updateBook(isbn):
    request_data = request.get_json()
    updated_book = {}
    if "title" in request_data:
        Book.updateBookTitle(isbn, request_data["title"])
    if "author" in request_data:
        Book.updateBookAuthor(isbn, request_data["author"])
    if "year" in request_data:
        Book.updateBookYear(isbn, request_data["year"])

    response = Response("", status=204)
    response.headers["Location"] = "/books/" + str(isbn)
    return response


@app.route("/books/<int:isbn>", methods=["DELETE"])
@token_required
def deleteBook(isbn):  # TODO: make this a soft delete -- don't delete from database
    #i = 0
    #for book in Book.getAllBooks():
        #if book["isbn"] == isbn:
            #Book.getAllBooks()[i] = {}
            #response = Response("", status=204)
            #return response
        #i += 1
    bookToDelete = Book.getBook(isbn)
    if Book.deleteBook(isbn):
        response = Response("", status=204)
        return response
    invalidBookObjectErrorMsg = {
        "error": "Book with given ISBN not found. Unable to delete as a result",
        "helpString": "Please provide an ISBN present in the list"
    }
    response = Response(json.dumps(invalidBookObjectErrorMsg), status=404, mimetype="application/json")
    return response


if __name__ == '__main__':
    app.run()
