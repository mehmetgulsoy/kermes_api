import functools
from flask_login import LoginManager, login_user, current_user, UserMixin, logout_user
from flask_socketio import disconnect
from app import bcrypt, login_manager
from .db import query_db, execute_db


class Uye(UserMixin):
  
  def __init__(self, sifre, durum='A', no=None, firma=None, uye=None, gorev=None, yetki=None, **kwargs):
    self.id = no
    self.sifre = sifre
    self.firma = firma
    self.gorev = gorev
    self.yetki = yetki
    self.uye = uye
    self.is_active = durum
    self.is_authenticated = False
    self.is_anonymous = True,
    self.ols_trh = None    
    for key, val in kwargs.items():
      setattr(self, key, val)
  
  @classmethod
  def fromFirmaUye(cls, firma, uye):
    res = query_db(
        'SELECT * FROM uye WHERE (firma= ? AND uye=?)', (firma, uye), True)
    if res:
        return cls(no=res['no'], sifre=res['sifre'], durum = res['durum'])
    else:
        None

  @classmethod
  def fromFirmaUye2(cls, firma, uye):
    res = query_db(
        'SELECT * FROM uye WHERE (firma= ? AND uye=?)', (firma, uye), True)
    if res:
        result = dict(res)
        return cls(**result)
    else:
        None      

  @classmethod
  def fromNoLoader(cls, no):
    """Flask-Login için loader olarak kullanılıyor."""
    res = query_db('SELECT no,sifre,durum,uye,firma FROM uye WHERE no=?', (no), True)
    if res:   
        uye = cls(**res)
        uye.is_authenticated = True
        uye.is_anonymous = False       
        return uye
    else:
        None

  def __repr__(self):
    return '<Uye {}>'.format(self.uye)  
      

  def uye_ekle(self):
    sifre = self.pw_hash()
    execute_db("""INSERT INTO uye (no,firma,uye,sifre,gorev,yetki) VALUES (null,?,?, ?,?, ?)""",
                (self.firma, self.uye, sifre, self.gorev, self.yetki))


  def uye_gnc(self, **kwargs):        
    sql = ""
    for key, val in kwargs.items():
      if key in ['gorev','yetki','durum']:
        sql+=f"{key} = {val} ,\n"
    else:
      sql = sql[0:-2]

    sql="UPDATE uye SET \n" + sql    
    sql +="where firma=? and uye=?"
    return sql

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

  def to_dict(self, include_password=False):
    data = {
      'no': self.id,
      'firma': self.firma,
      'uye': self.uye,
      'ols_trh': self.ols_trh,      
      'gorev': self.gorev,
      'yetki': self.yetki,
      'durum': self.is_active        
    }
    if include_password:
        data['sifre'] = self.sifre
    return data

  def from_dict(self, data, new_user=False):
    for field in ['no', 'firma', 'uye','gorev','yetki','durum','ols_trh']:
        if field in data:
            setattr(self, field, data[field])
    if new_user and 'sifre' in data:
        self.sifre = data['sifre']    


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


class Personel():
    def __init__(self, firma, uye):
        self.firma = firma
        self.uye = uye

    @classmethod
    def fromFirmaUye(cls, firma, uye):
        res = query_db(
            'SELECT * FROM uye WHERE (firma= ? AND uye=?)', (firma, uye), True)
        if res:
            return cls(res['firma'], res['uye'])
        else:
            None
