from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "123b123123bdfgdfgdsfsd123123"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////Users/Abdullah/Desktop/AKBLOG/blog.db"
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message_category = "info"

from blog import routes