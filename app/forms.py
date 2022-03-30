import re

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, \
    Email

required = 'Это обязательное поле'


def password_check(form, field):
    msg = 'Пароль должен содержать латинские сивмолы в верхнем и нижнем регистре и цифры'
    patern1 = re.compile('[a-z]+')
    patern2 = re.compile('[A-Z]+')
    patern3 = re.compile('\d+')
    if (not patern1.search(field.data) or
            not patern2.search(field.data) or
            not patern3.search(field.data)):
        raise ValidationError(msg)


class LoginForm(FlaskForm):
    email = StringField('Почта:', validators=[DataRequired()])
    password = PasswordField('Пароль:', validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    email = StringField(
        'Почта:',
        validators=[DataRequired(), Email('Неверный формат')]
    )
    password = PasswordField(
        'Пароль:',
        validators=[
            DataRequired(),
            Length(min=8, message='Пароль должен быть не менее 8 символов'),
            EqualTo('confirm_password', message='Пароли не одинаковые'),
            password_check
        ]
    )
    confirm_password = PasswordField('Пароль ещё раз:')


class ChangePasswordForm(FlaskForm):
    password = PasswordField(
        'Пароль:',
        validators=[
            DataRequired(),
            Length(min=8, message='Пароль должен быть не менее 8 символов'),
            EqualTo('confirm_password', message='Пароли не одинаковые'),
            password_check
        ]
    )
    confirm_password = PasswordField('Пароль ещё раз:')


class OrderForm(FlaskForm):
    username = StringField('Имя:', validators=[DataRequired(required)])
    address = StringField('Адрес:', validators=[DataRequired(required)])
    email = StringField(
        'Почта:',
        validators=[DataRequired(required),Email('Неверный формат')]
    )
    phone = StringField('Телефон:', validators=[DataRequired(required)])
