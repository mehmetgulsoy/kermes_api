from flask import request, render_template
from flask_login import LoginManager, login_user, current_user, logout_user
from . import main
from .model import Uye
from .db import query_db

@main.route('/')
def index():
  return render_template('index.html')


@main.route('/login', methods=["POST"])
def login():
  error = False
  msg  = ''

  if current_user.is_authenticated:
      return None    

  uye, firma = str.split(request.values.get('uye',''),'@')
  sifre = request.values.get('sifre','')

  if uye == '' or firma == '' or sifre == '' :
    return None    

  res = query_db('SELECT * FROM "uye" where uye = ? and firma = ?',(uye,firma), True)
  if res is None:
    return None
    
  uye = Uye(res['no'],'dfd','fdfdf')
  if uye is None or not uye.verify_password(sifre):
    return None
  else:
    login_user(uye, remember= False)
  
  return {'error': error, 'msg': msg}


@main.route('/logout')
def logout():
  error = False
  msg  = 'Çıkış yapıldı'
  logout_user()
  return {'error': error, 'msg': msg}