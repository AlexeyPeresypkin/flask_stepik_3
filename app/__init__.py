from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app.config import DevelopmentConfig
from app.models import db
from flask_migrate import Migrate
from app.models import User, Category, Dish, Order
from app.admin.models import MyUserView

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

db.init_app(app)
migrate = Migrate(app, db)
admin = Admin(app)

admin.add_view(MyUserView(User, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Dish, db.session))
admin.add_view(ModelView(Order, db.session))

from app.views import *
