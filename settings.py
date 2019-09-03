# used to store the settings/configs of the app
from flask import Flask

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///C:\\Users\\sfathir\\PycharmProjects\\BookREST/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
