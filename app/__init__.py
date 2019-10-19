import os
from flask import Flask
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt 
from flask_login import LoginManager
from config import Config

socketio = SocketIO()
login_manager = LoginManager()
bcrypt = Bcrypt()

def create_app(config_class=Config):
  """Flask uygulaması oluşturur."""
  app = Flask(__name__)
  app.config.from_object(config_class)

  bcrypt.init_app(app)
  login_manager.init_app(app) 
 
  from app.v_1_0 import db  
  db.init_app(app)

  from app.v_1_0 import main as main_blueprint
  app.register_blueprint(main_blueprint)
  from app.v_1_0 import events
  
  socketio.init_app(app, cors_allowed_origins='*')

  # ensure the instance folder exists
  try:
    os.makedirs(app.instance_path)
  except OSError:
    pass
  
  return app
