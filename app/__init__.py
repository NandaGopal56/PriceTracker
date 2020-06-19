from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)


app.config['SECRET_KEY'] = '28cd51a3bb2e0dbd90839a3d4e897f493fa13755'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.signin'
login_manager.login_message_category = 'info'
login_manager.init_app(app)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'pricetracker.info@gmail.com'
app.config['MAIL_PASSWORD'] = 'lyzwfewhkjodtppo'

mail = Mail(app)

from app.users.routes import users
from app.posts.routes import posts
from app.main.routes import main
from app.errors.handlers import errors
app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
app.register_blueprint(errors)


