# used to store the settings/configs of the app
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:\\Users\\sfathir\\PycharmProjects\\BookREST/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
