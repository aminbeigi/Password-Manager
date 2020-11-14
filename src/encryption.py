from cryptography.fernet import Fernet
import configparser

"""Symmetric key encryption

Using the Fernet recipie insdie the cyrptography library to encrypt passwords in password_manager.py
"""

### globals variables ###
CONFIG_FILE_PATH = 'config.ini'
config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)
KEY = config.get('MAIN', 'key')

class Encryption:
    def __init__(self):
        self.cipher = Fernet(KEY)
    
    def encrypt(self, plain_text):
        plain_text = plain_text.encode('utf-8')
        self.token = self.cipher.encrypt(plain_text)
        return self.token
    
    def decrypt(self):
        decoded = self.cipher.decrypt(self.token)
        return decoded

    def generate_key(self):
        self.key = Fernet.generate_key()