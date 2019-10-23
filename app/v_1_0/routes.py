from flask import request, render_template ,jsonify
from flask_login import LoginManager, login_user, current_user, logout_user
from . import main
from .model import Uye
from .db import query_db

@main.route('/')
def index():
  return render_template('index.html')


@main.route('/login', methods=["POST","GET"])
def login():
  if current_user.is_authenticated:
      return {'error': True, 'msg': 'Uye zaten login!'}   

  rq = request.get_json(force=True,silent=True)
  if rq['uye'].find('@') == -1:
    return {'error': True, 'msg': 'uye@firma formatında olmalı!'}   

  uye, firma = str.split(rq['uye'],'@')
  sifre = rq['sifre']

  if uye == '' or firma == '' or sifre == '' :
    return {'error': True, 'msg': 'Kullacıcı adı ve/veya şifre giriniz!'}    
    
  uye = Uye.fromFirmaUye(firma,uye)
  if uye is None or not uye.verify_password(sifre):
    return {'error': True, 'msg': 'Kullacıcı adı ve/veya şifre hatalı'}  
  else:
    login_user(uye, remember= False)
    return {'error': False, 'msg': 'Login oldunuz', 'data': {'uye': uye.get_id}} 

@main.route('/logout')
def logout():
  error = False
  msg  = 'Çıkış yapıldı'
  logout_user()
  return {'error': error, 'msg': msg}