from app import app, user_datastore
from app.models import db, Role


def create_test_user():
    user_role = Role(name='user')
    super_user_role = Role(name='superuser')
    db.session.add(user_role)
    db.session.add(super_user_role)

    test_user = user_datastore.create_user(
        email='admin@ya.ru',
        password='qwertY123',
        roles=[user_role, super_user_role]
    )

    db.session.commit()


with app.app_context():
    db.create_all()
    # create_test_user()
