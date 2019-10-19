import time
import sqlite3
import traceback
import logging
from flask import session, escape, g, jsonify
from flask_socketio import emit, join_room, leave_room
from flask_login import LoginManager, login_user, current_user, UserMixin
from .. import socketio, bcrypt
from .db import get_db,query_db, execute_db

@socketio.on('connect')
def connect():
  emit('connect_info',{'type': 'EMIT_CON', 'data': 'Connected'},broadcast=True)
  if current_user.is_authenticated:
    print('Server Side Client Connected is_authenticated ' + current_user.id) 
  else:
    print('Server Side Client Connected is not authenticated')   

@socketio.on('disconnect')
def disconnect():   
  print('Client Disconnected')   

@socketio.on('reconnect')
def reconnect():   
  print('Client reconnect')    

@socketio.on('uye_kayit')
def kayit(json): 
  time.sleep(3)
  error = True
  msg = [] 
   
  try:    
    con = get_db()
    with con:       
      param = json.get('firma'),json.get('unvan',''),json.get('eposta',''),json.get('telefon','')
      con.execute('INSERT INTO "FIRMA" (firma,unvan,eposta,telefon) VALUES (?,?,?,?)',param)

      sifre = json.get('sifre','')
      sifre_ozet = bcrypt.generate_password_hash(sifre).decode('utf-8')
      
      param = json.get('adi'),sifre_ozet ,json.get('firma'),'ADMIN'
      con.execute('INSERT INTO "UYE" (uye,sifre,firma,yetki) VALUES (?,?,?,?)',param)

    msg.append("Hesap başarıyla oluşturuldu. Lütfen Giriş Yap'ı tıklayın")
    error = False
  except sqlite3.IntegrityError:
    msg.append("Bu Hesap zaten var! Üyu girişi yapınız")  
  except :
    msg.append("Bilinmeyen hata oluştu. Tekrar Deneyin") 
    logging.error(traceback.format_exc())
  finally:   
    return {'error': error, 'msg': msg} 
  

@socketio.on('ping')
def ping():   
  print('Ping fired')    

@socketio.on('pong')
def pong(latency):   
  print('Pong fired',latency)   
  
@socketio.on_error()
def error_handler(e):
  print('Hata oluştu', e)  
