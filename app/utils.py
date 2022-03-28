from flask import session, redirect, url_for
from sqlalchemy import func

from app.models import Dish, db, Order


def give_dishes_and_total(cart):
    if not cart:
        return [], 0
    dishes = Dish.query.filter(Dish.id.in_(cart)).all()
    total = db.session.query(
        func.sum(Dish.price))\
        .filter(Dish.id.in_(cart))\
        .first()
    return dishes, total[0]


def write_obj_in_db(form, total, dishes):
    if not session.get('user'):
        return redirect(url_for('auth_view'))
    user_id = session['user']['id']
    order_obj = Order(
        total_sum=total,
        status='Ordered',
        email=form.email.data,
        phone=form.phone.data,
        address=form.address.data,
        user_id=user_id
    )
    db.session.add(order_obj)
    for dish in dishes:
        order_obj.dishes.append(dish)
    db.session.commit()
