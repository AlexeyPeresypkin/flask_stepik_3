from flask import Flask
from views import *
from app.config import DevelopmentConfig
from app.models import db

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db.init_app(app)


