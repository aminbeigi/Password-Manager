from cryptography.fernet import Fernet
from my_configparser import MyConfigParser

"""Symmetric key encryption

Using the Fernet recipie via the cyrptography module to encrypt passwords in main.py.
"""

### globals variables ###
CONFIG = MyConfigParser()
KEY = CONFIG.get('MAIN', 'key')

class Encryption:
    def encrypt(self, message):
        message = message.encode() # to bytes
        return Fernet(KEY).encrypt(message)    

    def decrypt(self, token):
        token = token.encode() # to bytes
        return Fernet(KEY).decrypt(token)