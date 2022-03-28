import datetime
from functools import wraps

from flask import abort, flash, session, redirect, request, render_template, \
    url_for

from sqlalchemy import func, select
from sqlalchemy.orm import joinedload

from app import app, db
from app.models import User, Category, Dish, Order
from app.forms import *
from app.utils import give_dishes_and_total, write_obj_in_db


@app.route('/')
def index_view():
    categories = Category.query.join(Dish).all()
    dishes, total = give_dishes_and_total(
        session.get('cart', [])
    )
    return render_template(
        'main.html',
        categories=categories,
        total=total,
        dishes=dishes
    )


@app.route('/cart', methods=['GET', 'POST'])
def cart_view():
    form = OrderForm()
    dishes, total = give_dishes_and_total(
        session.get('cart', [])
    )

    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template(
                'cart.html',
                total=total,
                dishes=dishes,
                form=form
            )
        if not total:
            flash('Вы ничего не добавили в корзину')
            return redirect(url_for('index_view'))
        write_obj_in_db(form, total, dishes)
        session['cart'] = []
        return render_template('ordered.html')

    return render_template(
        'cart.html',
        total=total,
        dishes=dishes,
        form=form
    )


@app.route('/addtocart/<int:dish_id>')
def add_to_cart_view(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    cart = session.get('cart', [])
    if dish_id not in cart:
        cart.append(dish_id)
        session['cart'] = cart
    return redirect(url_for('index_view'))


@app.route('/delete/<int:dish_id>')
def delete_from_cart_view(dish_id):
    dish = Dish.query.get_or_404(dish_id)
    cart = session.get('cart', [])
    if dish_id in cart:
        cart.remove(dish_id)
        session['cart'] = cart
        flash('Блюдо удалено из корзины')
    return redirect(url_for('cart_view'))


@app.route('/account')
def account_view():
    dishes, total = give_dishes_and_total(
        session.get('cart', [])
    )
    if session.get('user'):
        user_id = session['user']['id']
        user = User.query.get_or_404(user_id)
        orders = Order.query.filter_by(user_id=user.id).all()
        return render_template('account.html',
                               total=total,
                               dishes=dishes,
                               orders=orders,
                               )
    return redirect(url_for('auth_view'))


@app.route('/auth', methods=['GET', 'POST'])
def auth_view():
    if session.get('user'):
        return redirect(url_for('account_view'))

    form = LoginForm()

    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('login.html', form=form)

        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password_valid(form.password.data):
            session['user'] = {
                'id': user.id,
                'email': user.email,
                'role': user.role,
            }
            return redirect(url_for('account_view'))

        form.email.errors.append('Неверное имя или пароль')

    return render_template('login.html', form=form)


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
        return redirect(url_for('auth_view'))

    return render_template('register.html', form=form)


@app.route('/logout')
def logout_view():
    session.pop('user')
    return redirect(url_for('auth_view'))


@app.route('/ordered')
def ordered_view():
    return render_template('ordered.html')
