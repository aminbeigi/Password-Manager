from cryptography.fernet import Fernet
from .static_config_parser import *

"""Symmetric key encryption

Using the Fernet recipie from the cyrptography module to encrypt passwords in main.py.
"""

class Encryption:
    def encrypt(self, message, key):
        message = message.encode() # to bytes
        return Fernet(key).encrypt(message)   

    def decrypt(self, token, key):
        token = token.encode() # to bytes
        return Fernet(key).decrypt(token).decode() # return string
    
    # Generating a key for config.ini
    def generate_key(self):
        return Fernet.generate_key()