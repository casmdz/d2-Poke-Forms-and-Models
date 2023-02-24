from flask import Flask 
from config import Config
from .models import db, User
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
# login_manager.init_app(app) this is the same as (app), we are doing the db.init(app) in models.py

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)  #added .query from aqlalchemy

login_manager.login_view = 'auth.loginPage'


from . import routes 
from . import models