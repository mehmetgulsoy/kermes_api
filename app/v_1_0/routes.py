from flask import render_template
from flask_login import LoginManager, login_user, current_user, UserMixin
from . import main
from .model import Uye

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login')
def login():
    uye = Uye("Mehmet Gülsoy","12", True)
    return login_user(uye)   