import mysql.connector
from mysql.connector import errorcode
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

### tables
TABLES = {}
TABLES['user_entries'] = (
    "CREATE TABLE `user_entries` ("
    "  `entry_no` varchar(50) NOT NULL,"
    "  `title` varchar(50) NOT NULL,"
    "  PRIMARY KEY (`entry_no`)"    
    ") ENGINE=InnoDB")

class Database:
    def __init__(self):
        # set up connection with database
        try:
            self.cnx = mysql.connector.connect(
                user=USER,
                password=PASSWORD,
                host=HOST,
                database=DATABASE
            )
            self.cursor = self.cnx.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        self.create_tables()        

    def create_tables(self):
        for table_name in TABLES:
            table_description = TABLES[table_name]
            try:
                print("Creating table {}: ".format(table_name), end='')
                self.cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")   

    def insert(self):
        add_entry = ("INSERT INTO user_entries "
                    "(entry_no, title) "
                    "VALUES (%s, %s)") 

        data_entry = ('3', 'cat')

        # insert new entry 
        self.cursor.execute(add_entry, data_entry)

        self.cnx.commit
        print("did it")

def main():
    db = Database()
    db.insert()
 

if __name__ == '__main__':
    main()    