import configparser
"""A config parser that is used by the modules main, database and encryption."""

class StaticConfigParser():
    CONFIG_FILE_PATH = './config/config.ini'
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    
    @staticmethod
    def get(parent, child):
        return StaticConfigParser.config.get(parent, child)