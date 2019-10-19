import os
from flask import current_app
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(16)
    DATABASE = os.path.join(basedir,'instance', "kermes.sqlite.db")
    DEBUG = True  
    ADMINS = ['your-email@example.com']
 
 
