from cryptography.fernet import Fernet
from .static_config_parser import StaticConfigParser

"""Symmetric key encryption

Using the Fernet recipie from the cyrptography module to encrypt passwords.
This module is used to encrypt and decrypt passwords in database.py.
"""

class Encryption:
    def encrypt(self, message, key):
        return Fernet(key).encrypt(message.encode()) # returns bytes

    def decrypt(self, token, key):
        return Fernet(key).decrypt(token.encode()).decode() # returns string
    
    # generating a key for config.ini
    def generate_key(self):
        return Fernet.generate_key()