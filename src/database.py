import mysql.connector
from mysql.connector import errorcode
import configparser
# local files
import encryption

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

### SQL code to create tables
TABLES = {}
TABLES['user_entries'] = (
    "CREATE TABLE `user_entries` ("
    "  `entry_no` char(3) NOT NULL,"
    "  `title` varchar(250) NOT NULL,"
    "  `username` varchar(250),"
    "  `password` varchar(250) NOT NULL,"
    "  `email` varchar(250) NOT NULL,"    
    "  PRIMARY KEY (`entry_no`)"    
    ") ENGINE=InnoDB")

class Database:
    def __init__(self):
        # initialise encryption object
        self.encryption = encryption.Encryption()

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
          
        self.create_table()   

    def create_table(self):
        for table_name in TABLES:
            print(table_name)
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

    def insert(self, title, username, password, email):
        add_entry = ("INSERT INTO user_entries "
                    "(entry_no, title, username, password, email) "
                    "VALUES (%s, %s, %s, %s, %s)") 

        encrypted_password = self.encryption.encrypt(password)

        data_entry = ((str(int(self.get_highest_id())+1)), title, username, encrypted_password, email)
        
        # insert new entry 
        self.cursor.execute(add_entry, data_entry)

        self.cnx.commit()

    def select_entries(self):
        # select all entry_no, title columns from database
        query = ("SELECT entry_no, title FROM user_entries")
        self.cursor.execute(query)
        output = self.cursor.fetchall()
        return output

    def get_entry(self, entry_no):
        # select all columns from database
        query = (f"""SELECT * FROM user_entries 
                WHERE entry_no = '{entry_no}'""")
        self.cursor.execute(query)
        output = self.cursor.fetchall()
        return output

    def get_password(self, entry_no):
        # selects...
        query = (f"""SELECT password FROM user_entries 
                WHERE entry_no = '{entry_no}'""")
        self.cursor.execute(query)
        output = self.cursor.fetchall()[0][0]
        decrypted_password = self.encryption.decrypt(output)
        return decrypted_password.decode() # change from bytes to string

    def get_highest_id(self):
        query = (f"SELECT MAX(entry_no) FROM user_entries")
        self.cursor.execute(query)
        output = self.cursor.fetchall()[0][0]

        if (output != None):
            return output
        else:
            return 0

def main():
    db = Database()
    db.insert('bob jane2', 'steve123', 'p@ssw0rd', 'me@aminbeigi.com')

if __name__ == '__main__':
    main()