import functools
from flask_login import LoginManager, login_user, current_user, UserMixin, logout_user
from flask_socketio import disconnect
from app  import bcrypt, login_manager 
from .db import query_db


class Uye(UserMixin):
  def __init__(self, no, sifre, durum):
    self.id = no
    self.sifre = sifre
    self.is_active = durum
    self.is_authenticated = False
    self.is_anonymous = True  

  @classmethod
  def fromFirmaUye(cls, firma, uye):
    res = query_db('SELECT * FROM uye WHERE (firma= ? AND uye=?)',(firma,uye),True)    
    return cls(res['no'],res['sifre'],res['durum'])

  @classmethod
  def fromNoLoader(cls, no):
    res = query_db('SELECT * FROM uye WHERE no=?',(no),True)
    if res: 
      uye = cls(res['no'],res['sifre'],res['durum']) 
      uye.is_authenticated = True 
      uye.is_anonymous     = False
      return uye 
    else:
      None

  @property
  def is_active(self):
    return self._is_active
     
  @is_active.setter 
  def is_active(self, value):           
    self._is_active = value == 'A'

  @property
  def is_authenticated(self):
    return self._is_authenticated

  @is_authenticated.setter
  def is_authenticated(self, value):
    self._is_authenticated = value    

  @property
  def is_anonymous(self):
    return self._is_anonymous  
  
  @is_anonymous.setter
  def is_anonymous(self, value):
    self._is_anonymous = value 

  
  def verify_password(self, password_in):
    """Verify the given password with the stored password hash"""
    chk = bcrypt.check_password_hash(self.sifre, password_in)
    self.is_authenticated = chk
    self.is_anonymous = not chk 
    return chk   

  def pw_hash(self):
    """Girilen şifreden özetli şifre oluşturur."""
    return bcrypt.generate_password_hash(self.sifre).decode('utf-8')  


def authenticated_only(f):
  @functools.wraps(f)
  def wrapped(*args, **kwargs):
      if not current_user.is_authenticated:
          disconnect()
          logout_user()
      else:
          return f(*args, **kwargs)
  return wrapped

@login_manager.user_loader
def user_loader(no): 
  return Uye.fromNoLoader(no) 
