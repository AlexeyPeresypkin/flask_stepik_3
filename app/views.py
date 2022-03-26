from functools import wraps

from flask import abort, flash, session, redirect, request, render_template

from app import app, db
from app.models import User
from app.forms import *


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/cart')
def cart():
    return render_template('cart.html')


@app.route('/account')
def account():
    return render_template('account.html')


@app.route('/auth')
def auth():
    return render_template('auth.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/logout')
def logout():
    return render_template('main.html')


@app.route('/ordered')
def ordered():
    return render_template('ordered.html')
