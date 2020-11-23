from cryptography.fernet import Fernet
import configparser

"""Symmetric key encryption

Using the Fernet recipie via the cyrptography module to encrypt passwords in main.py.
"""

### globals variables ###
CONFIG_FILE_PATH = 'config.ini'
config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)
KEY = config.get('MAIN', 'key')

class Encryption:
    def encrypt(self, message):
        message = message.encode() # to bytes
        return Fernet(KEY).encrypt(message)    

    def decrypt(self, token):
        token = token.encode()
        return Fernet(KEY).decrypt(token)