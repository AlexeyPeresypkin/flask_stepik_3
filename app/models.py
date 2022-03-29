import datetime

from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()


orders_dishes_association = db.Table(
    'orders_dishes',
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id')),
    db.Column('dish_id', db.Integer, db.ForeignKey('dishes.id')),
)

categories_dishes_association = db.Table(
    'categories_dishes',
    db.Column('category_id', db.Integer, db.ForeignKey('categories.id')),
    db.Column('dish_id', db.Integer, db.ForeignKey('dishes.id')),
)

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    orders = db.relationship('Order', )

    @property
    def password(self):
        raise AttributeError("Вам не нужно знать пароль!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def password_valid(self, password):
        return check_password_hash(self.password_hash, password)


class Dish(db.Model):
    __tablename__ = 'dishes'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    picture = db.Column(db.String)

    category_id = db.Column(
        db.Integer,
        db.ForeignKey('categories.id')
    )
    category = db.relationship('Category')
    orders = db.relationship(
        'Order',
        secondary=orders_dishes_association,
        back_populates='dishes'
    )


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    dishes = db.relationship('Dish', viewonly=True)


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    total_sum = db.Column(db.Integer)
    status = db.Column(db.String)
    email = db.Column(db.String(32), nullable=False)
    phone = db.Column(db.String)
    address = db.Column(db.String)

    dishes = db.relationship(
        'Dish', secondary=orders_dishes_association, back_populates='orders'
    )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), default=None)
    user = db.relationship('User', viewonly=True)
