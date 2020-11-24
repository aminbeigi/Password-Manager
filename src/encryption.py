from cryptography.fernet import Fernet
import static_config_parser

"""Symmetric key encryption

Using the Fernet recipie from the cyrptography module to encrypt passwords in main.py.
"""

### globals variables ###
CONFIG = static_config_parser.StaticConfigParser()
KEY = CONFIG.get('MAIN', 'key')

class Encryption:
    def encrypt(self, message):
        message = message.encode() # to bytes
        return Fernet(KEY).encrypt(message)    

    def decrypt(self, token):
        token = token.encode() # to bytes
        return Fernet(KEY).decrypt(token)
    
    # Generating a key for config.ini
    def generate_key(self):
        return Fernet.generate_key()