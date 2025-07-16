import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

app = Flask(__name__)
app.secret_key = "a-very-secret-key-for-development"
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# SQLite ডাটাবেস ব্যবহার করার জন্য কনফিগারেশন
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login' # লগইন না করা থাকলে এই রুটে পাঠাবে
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.query.get(int(user_id))

# এই অংশটি ডাটাবেস টেবিল তৈরি করে
with app.app_context():
    import models
    db.create_all()

# রাউটগুলো ইম্পোর্ট করা হচ্ছে
from routes import *