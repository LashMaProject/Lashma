import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from models import db
# Configuration
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# database connection
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") 
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config['UPLOAD_FOLDER'] = 'uploads'  # Where to temporarily save uploaded images
# Move this line back to the same indentation level as the previous one
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# mail config
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME") 
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

db.init_app(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()
# routes
from routes import *
