import datetime

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


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(32), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), nullable=False, default='usr')
    orders = db.relationship('Order')

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

    categories = db.relationship(
        'Category',
        secondary=categories_dishes_association,
        back_populates='dishes'
    )
    orders = db.relationship(
        'Order',
        secondary=orders_dishes_association,
        back_populates='dishes'
    )


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

    dishes = db.relationship(
        'Dish',
        secondary=categories_dishes_association,
        back_populates='categories'
    )


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    total_sum = db.Column(db.Integer)
    status = db.Column()
    email = db.Column(db.String(32), nullable=False)
    phone = db.Column()
    address = db.Column()

    dishes = db.relationship(
        'Dish', secondary=orders_dishes_association, back_populates='orders'
    )
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User')
