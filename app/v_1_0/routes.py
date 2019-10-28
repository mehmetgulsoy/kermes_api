import time
import sqlite3
import traceback
import logging
from flask import request
from flask_login import login_user, current_user, logout_user, login_required
from app.v_1_0 import main
from app.v_1_0.model import Uye
from app.v_1_0.db import query_db, execute_db
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


@main.route('/urun_katagori', methods=["GET"])
@login_required
def urun_katagori():
  #https://stackoverflow.com/questions/3286525/return-sql-table-as-json-in-python  
  firma = current_user.firma
  cur = query_db("select deger as katagori from firma_data where anahtar='menu_katagori' and  firma=?",(firma,),True) or {}  
  return success_request('urun katagori listesi',dict(cur))  

@main.route('/urun_ekle', methods=["POST"])
@login_required
def urun_ekle():  
  data = request.get_json(silent=True) or {}
  if 'adi' not in data or 'taksim' not in data or 'fiyat' not in data:     
    return bad_request('adi, katagori ve fiyat zorunlu alandır!') 
  
  firma = current_user.firma
  urun = data.get('adi','') 
  aciklama = data.get('aciklama','') 
  durum = data.get('aktif', True)  
  miktar = data.get('eldeki',0) 
  fiyat = data.get('fiyat',0)   
  stok_takip = data.get('takip', False) 
  taksim = data.get('taksim','')

  try:
    execute_db("""INSERT INTO URUN (firma,urun,aciklama,fiyat,miktar,stok_takip,durum,katagori) 
                VALUES (?,?,?,?,?,?,?,?)""",(firma,urun,aciklama,fiyat,miktar,stok_takip,durum,taksim))  
    return success_request('Urun eklendi.')
  except sqlite3.IntegrityError:
    execute_db("""UPDATE "URUN" SET aciklama=?,katagori=?,fiyat=?,miktar=?,stok_takip=?,durum=? 
                  WHERE (firma=? AND urun=?)""", 
                  (aciklama,taksim,fiyat,miktar,stok_takip,durum,firma,urun))  
    return success_request('Urun güncellendi.')
  except : 
    logging.error(traceback.format_exc())
    return bad_request('İşlem başarısız.')
