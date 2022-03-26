from functools import wraps

from flask import abort, flash, session, redirect, request, render_template

from app import app, db
from app.models import User
from app.forms import *
__all__ = []


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/cart')
def index():
    return render_template('cart.html')


@app.route('/account')
def index():
    return render_template('account.html')


@app.route('/auth')
def index():
    return render_template('auth.html')


@app.route('/register')
def index():
    return render_template('register.html')


@app.route('/logout')
def index():
    return render_template('main.html')


@app.route('/ordered')
def index():
    return render_template('ordered.html')
