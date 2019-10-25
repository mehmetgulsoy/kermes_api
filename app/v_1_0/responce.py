from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

def response(status_code, message=None, data=None, meta=None):
  payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
  if message:
      payload['msg'] = message
  if data:
      payload['data'] = data
  if meta:
    payload['meta'] = meta    

  response = jsonify(payload)
  response.status_code = status_code
  return response


def bad_request(message):
  return response(400, message)

def success_request(message=None, data=None, meta=None):
    return response(200, message, data, meta)

def warning_request(message):
  return response(100, message)