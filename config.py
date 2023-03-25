from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import os

app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/security"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

db = SQLAlchemy(app)

Session(app)