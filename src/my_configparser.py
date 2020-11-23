import configparser

class MyConfigParser():
    def __init__(self):
        CONFIG_FILE_PATH = 'config.ini'
        self.config = configparser.ConfigParser() 
        self.config.read(CONFIG_FILE_PATH)
    
    def get(self, parent, child):
        return(self.config.get(parent, child))