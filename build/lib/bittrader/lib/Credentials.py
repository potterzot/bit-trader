import base64
import time

class Credentials:
  def __init__(self, api_key, secret):
    self.setApiKey(api_key)
    self.setSecret(secret)

  def setApiKey(self, api_key):
    self.api_key = api_key

  def setSecret(self, secret):
    self.secret = secret
    self.decoded_secret = base64.b64decode(secret)

  def getApiKey(self):
    return self.api_key

  def getSecret(self):
    return self.decoded_secret

  def getNonce(self):
      return int(time.time()*100000)

