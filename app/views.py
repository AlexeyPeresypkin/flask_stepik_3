import datetime
from functools import wraps

from flask import abort, flash, session, redirect, request, render_template, \
    url_for
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from app import app, db
from app.models import User, Category, Dish, Order
from app.forms import *
from app.utils import give_dishes_and_total, write_obj_in_db


@app.route('/')
def index_view():
    categories = Category.query.join(Dish).all()
    cart, total = session.get('cart', []), 0
    if cart:
        dishes, total = give_dishes_and_total(cart)
    return render_template(
        'main.html',
        categories=categories,
        total=total[0],
        dishes=dishes
    )


@app.route('/cart', methods=['GET', 'POST'])
def cart_view():
    form = OrderForm()
    cart, total = session.get('cart', []), 0
    if cart:
        dishes, total = give_dishes_and_total(cart)

    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template(
                'cart.html',
                total=total[0],
                dishes=dishes,
                form=form
            )
        if not cart:
            return redirect(url_for('index_view'))
        write_obj_in_db(form, total, dishes)
        return render_template('ordered.html')

    return render_template(
        'cart.html',
        total=total[0],
        dishes=dishes,
        form=form
    )


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


@app.route('/register', methods=['GET', 'POST'])
def register_view():
    form = RegistrationForm()

    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('register.html', form=form)

        user = User.query.filter_by(email=form.email.data).first()
        if user:
            form.email.errors.append(
                'Пользователь с такой почтой уже существует')
            return render_template('register.html', form=form)

        user = User()
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()

        flash(
            f'Пользователь: {form.email.data} с паролем: {form.password.data} зарегистрирован')
        return redirect(url_for('account_view'))

    return render_template('register.html', form=form)


@app.route('/logout', methods=['POST'])
def logout_view():
    session.pop('user')
    return redirect(url_for('auth_view'))


@app.route('/ordered')
def ordered_view():
    return render_template('ordered.html')
