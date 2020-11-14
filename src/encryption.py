
"""Symmetric key encryption

Using the Fernet recipie insdie the cyrptography library to encrypt passwords in password_manager.py
"""
from cryptography.fernet import Fernet

class Encryption:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)
    
    def encrypt(self, plain_text):
        plain_text = plain_text.encode('utf-8')
        self.token = self.cipher.encrypt(plain_text)
        return self.token
    
    def decrypt(self):
        decoded = self.cipher.decrypt(self.token)
        return decoded