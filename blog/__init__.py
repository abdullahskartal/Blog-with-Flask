from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "5791628bb0b13ce0c676dfde280ba245"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////Users/Abdullah/Desktop/AKBLOG/blog.db"
db = SQLAlchemy(app)

from blog import routes