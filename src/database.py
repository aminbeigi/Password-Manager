import mysql.connector
import configparser

"""The database

This is an epic database.
"""

### globals variables ###
CONFIG_FILE_PATH = 'config.ini'
config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH)

USER = config.get('mySQL', 'user')
PASSWORD = config.get('mySQL', 'password')
HOST = config.get('mySQL', 'host')
DATABASE = config.get('mySQL', 'database')

class Database:
    def __init__(self):
        cnx = mysql.connector.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            database=DATABASE
        )