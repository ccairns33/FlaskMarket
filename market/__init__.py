from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///market.db"
# to display form html
app.config['SECRET_KEY'] = 'a9989de36247ea226d7bd1f0'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
from market import routes