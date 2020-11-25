from cryptography.fernet import Fernet
from .static_config_parser import *

"""Symmetric key encryption

Using the Fernet recipie from the cyrptography module to encrypt passwords in main.py.
"""

class Encryption:
    def encrypt(self, message, key):
        return Fernet(key).encrypt(message.encode()) # returns bytes

    def decrypt(self, token, key):
        return Fernet(key).decrypt(token.encode()).decode() # returns string
    
    # Generating a key for config.ini
    def generate_key(self):
        return Fernet.generate_key()