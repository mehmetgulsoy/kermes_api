import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext

def query_db(query, args=(), one=False):
  """sql komutu koşturur ve data geriye döner."""
  cur = get_db().execute(query, args)
  cur.execute(query, args)
  rv = cur.fetchall()
  cur.close()
  return (rv[0] if rv else None) if one else rv

def execute_db(query, args=()):
  """sql komutu koşturur."""
  con = get_db()
  with con:     
    con.execute(query, args)
  

def get_db():
  """Db bağlantısını geri döner."""
  if 'db' not in g:
    g.db = sqlite3.connect(
      current_app.config['DATABASE'],
      detect_types=sqlite3.PARSE_DECLTYPES
    )
    g.db.row_factory = sqlite3.Row
  return g.db

def close_db(e=None):
  """Db bağlantısını kapatır.."""
  db = g.pop('db', None)

  if db is not None:
    db.close()

def init_db():
  """schema.sql'i execute eder."""
  db= get_db()
  with current_app.open_resource('schema.sql') as f:
    db.executescript(f.read().decode('utf-8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
  """Tabloları drop edip tekrar oluşturur"""
  init_db()
  click.echo('Database oluşturuldu.')

def init_app(app):
  app.teardown_appcontext(close_db)
  app.cli.add_command(init_db_command)