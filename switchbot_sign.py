import base64
import hashlib
import hmac
import time
import uuid


def create_headers(token: str, secret: str):
  headers = {}
  
  nonce = uuid.uuid4()
  t = int(round(time.time() * 1000))
  string_to_sign = '{}{}{}'.format(token, t, nonce)

  string_to_sign = bytes(string_to_sign, 'utf-8')
  secret = bytes(secret, 'utf-8')

  sign = base64.b64encode(
      hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
  
  headers['Authorization'] = token
  headers['Content-Type'] = 'application/json'
  headers['charset'] = 'utf8'
  headers['t'] = str(t)
  headers['sign'] = sign
  headers['nonce'] = str(nonce)
  
  return headers