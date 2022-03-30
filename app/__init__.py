from flask import Flask
from flask_admin import Admin
from flask_migrate import Migrate
from flask_security import SQLAlchemyUserDatastore, Security

from app.admin.models import MyUserView, MyDishView, MyCategoryView, \
    MyOrderView
from app.config import DevelopmentConfig
from app.models import User, Category, Dish, Order, Role
from app.models import db

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)
migrate = Migrate(app, db)
admin = Admin(app)
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

admin.add_view(MyUserView(User, db.session))
admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyDishView(Dish, db.session))
admin.add_view(MyOrderView(Order, db.session))
from app.views import *
