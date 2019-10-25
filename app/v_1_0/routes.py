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
      return {'error': False, 'msg': 'Uye zaten login!'},200   

  data = request.get_json() 
  
  if data['uye'] and data['sifre']: 
    uye = data.get('uye','')
    if '@' not in uye:
      return {'error': True, 'msg': 'uye@firma formatında olmalı!'}, 400   

    uye, firma = str.split(uye,'@')
    sifre = data.get('sifre')

    if not uye or not firma or not sifre:
      return {'error': True, 'msg': 'Kullacıcı adı ve/veya şifre giriniz!'},400    
    
    uye = Uye.fromFirmaUye(firma,uye)
    if uye is None or not uye.verify_password(sifre):
      return {'error': True, 'msg': 'Kullacıcı adı ve/veya şifre hatalı'},400  
    else:
      ogin_user(uye, remember= False)
      return jsonify({'error': False, 'msg': 'Login oldunuz', 'data': {'uye': uye.get_id()}}),200 

@main.route('/logout')
def logout():
  error = False
  msg  = 'Çıkış yapıldı'
  logout_user()
  return {'error': error, 'msg': msg}