from sqlalchemy import func

from app.models import Dish, db, Order


def give_dishes_and_total(cart):
    dishes = Dish.query.filter(Dish.id.in_(cart)).all()
    total = db.session.query(
        func.sum(Dish.price))\
        .filter(Dish.id.in_(cart))\
        .group_by(Dish.category_id)\
        .first()
    return dishes, total


def write_obj_in_db(form, total, dishes):
    order_obj = Order(
        total_sum=total[0],
        status='Ordered',
        email=form.email.data,
        phone=form.phone.data,
        address=form.address.data,
    )
    db.session.add(order_obj)
    for dish in dishes:
        order_obj.dishes.append(dish)
    db.session.commit()
