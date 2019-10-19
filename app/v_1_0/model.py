import functools
from flask_login import LoginManager, login_user, current_user, UserMixin
from flask_socketio import disconnect
from app  import bcrypt, login_manager 
from .db import query_db



class Uye(UserMixin):
  def __init__(self, no, sifre, durum):
    self.id = no
    self.sifre = sifre
    self.durum = durum
  
  @property
  def is_active(self):
    return self.durum  

  @property
  def is_authenticated(self):
      return self.is_authenticated

  @property
  def is_anonymous(self):
    return not self.is_authenticated  
  
  
  def verify_password(self, password_in):
    """Verify the given password with the stored password hash"""
    return bcrypt.check_password_hash(self.sifre, password_in)    

  def pw_hash(self):
    """Girilen şifreden özetli şifre oluşturur."""
    return bcrypt.generate_password_hash(self.sifre).decode('utf-8')  

    

def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped

@login_manager.user_loader
def user_loader(no):
  uye = query_db('SELECT * FROM uye where no = ?',(no,)) 
  #Uye(no)
  return uye 
