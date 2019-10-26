from flask import request
from flask_login import login_user, current_user, logout_user, login_required
from app.v_1_0 import main
from app.v_1_0.model import Uye
from app.v_1_0.db import query_db
from app.v_1_0.responce import bad_request, success_request

@main.route('/login', methods=["POST","GET"])
def login():
  if current_user.is_authenticated:      
      return success_request('Zaten login oldunuz.')   
  
  data = request.get_json(silent=True) or {}
  if 'uye' not in data or 'sifre' not in data:     
    return bad_request('uye ve/veya sifre gerekli!') 

  if '@' not in data['uye']:
    return bad_request('uye@firma formatında olmalı!') 
 
  uye, firma = str.split(data['uye'],'@',1)
  sifre = data['sifre']

  if not uye or not firma or not sifre:
    return bad_request('Kullanıcı adı ve/veya şifre hatalı!')    
    
  uye = Uye.fromFirmaUye(firma,uye)
  if uye is None or not uye.verify_password(sifre):
    return bad_request('Kullacıcı adı ve/veya şifre eşleşmedi.!')  
  else:
    login_user(uye)
    data = { 'uye': uye.get_id() }
    return success_request('Login oldunuz',data)

@main.route('/logout')
def logout():
  logout_user()
  return success_request() 


@main.route('/urun', methods=["GET"])
@login_required
def menu_item():  
  firma = current_user.firma
  data = query_db('select * from "urun" where firma=?',(firma,),True) or {}
  return success_request('urun listesi',data)

@main.route('/urun_ekle', methods=["POST"])
@login_required
def urun_ekle():
  data = request.get_json(silent=True) or {}
  if 'uye' not in data or 'sifre' not in data:     
    return bad_request('uye ve/veya sifre gerekli!') 

 
  uye, firma = str.split(data['uye'],'@',1)
  sifre = data['sifre']

  if not uye or not firma or not sifre:
    return bad_request('Kullanıcı adı ve/veya şifre hatalı!')    
    
  uye = Uye.fromFirmaUye(firma,uye)
  if uye is None or not uye.verify_password(sifre):
    return bad_request('Kullacıcı adı ve/veya şifre eşleşmedi.!')  
  else:
    login_user(uye)
    data = { 'uye': uye.get_id() }
    return success_request('Login oldunuz',data)
