import configparser

class StaticConfigParser():
    CONFIG_FILE_PATH = 'config.ini'
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_PATH)
    
    @staticmethod
    def get(parent, child):
        return StaticConfigParser.config.get(parent, child)