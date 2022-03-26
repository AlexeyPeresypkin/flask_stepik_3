from functools import wraps

from flask import abort, flash, session, redirect, request, render_template, \
    url_for
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from app import app, db
from app.models import User, Category, Dish
from app.forms import *


@app.route('/')
def index_view():
    categories = Category.query.join(Dish).all()
    # dishes = Dish.query.join(Category).all()
    # print(dishes)
    # for dish in dishes:
    #     print(dish.category.title)
    print(categories)
    # for category in categories:
    #     # pass
    #     print(category.dishes[:3])
    #     # print(dish.dishes)
    return render_template('main.html', categories=categories)


@app.route('/cart')
def cart_view():
    cart = session.get('cart', [])
    if cart:
        dishes = Dish.query.filter(Dish.id.in_(cart)).all()
        total = db.session.query(
            func.sum(Dish.price)
                ).filter(Dish.id.in_(cart)
                ).group_by(Dish.category_id
                ).first()
    return render_template('cart.html', total=total[0], dishes=dishes)


@app.route('/addtocart/<int:dish_id>')
def add_to_cart_view(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    cart = session.get('cart', [])
    cart.append(dish_id)
    session['cart'] = cart
    return redirect(url_for('cart_view'))


@app.route('/account')
def account_view():
    return render_template('account.html')


@app.route('/auth')
def auth_view():
    return render_template('auth.html')


@app.route('/register')
def register_view():
    return render_template('register.html')


@app.route('/logout')
def logout_view():
    return render_template('main.html')


@app.route('/ordered')
def ordered_view():
    return render_template('ordered.html')
