import mysql.connector
from mysql.connector import errorcode
from .encryption import Encryption
from .static_config_parser import StaticConfigParser

"""The mySQL database holding all user entries

The mySQL database will hold one table 'user_entries' that will contain all the entries
the user has inputted in main.py.
"""

### globals variables ###
CONFIG = StaticConfigParser()

USER = CONFIG.get('mySQL', 'user')
PASSWORD = CONFIG.get('mySQL', 'password')
HOST = CONFIG.get('mySQL', 'host')
DATABASE = CONFIG.get('mySQL', 'database')

### encryption
KEY = CONFIG.get('MAIN', 'key')

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
        self.encryption = Encryption()

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
            try:
                print("Creating table {}: ".format(table_name), end='')
                self.cursor.execute(TABLES[table_name])
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

        encrypted_password = self.encryption.encrypt(password, KEY)

        data_entry = ((str(int(self.get_highest_id())+1)), title, username, encrypted_password, email)
        
        # insert new entry
        self.cursor.execute(add_entry, data_entry)

        self.cnx.commit()

    def select_all_entry_no_and_title(self):
        # select ALL rows with 'entry_no' and 'title' columns from database
        query = ("SELECT entry_no, title FROM user_entries")
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_title(self, entry_no):
        # select a row from database
        query = (f"""SELECT title FROM user_entries 
                WHERE entry_no = '{entry_no}'""")
        self.cursor.execute(query)
        return self.cursor.fetchall()[0][0]  

    def get_username(self, entry_no):
        # select a row from database
        query = (f"""SELECT username FROM user_entries 
                WHERE entry_no = '{entry_no}'""")
        self.cursor.execute(query)
        output = self.cursor.fetchall()[0][0]
        
        # user has not entered a username
        if (output == ''):
            return 'N/A'
        return output   

    def get_email(self, entry_no):
        # select a row from database
        query = (f"""SELECT email FROM user_entries 
                WHERE entry_no = '{entry_no}'""")
        self.cursor.execute(query)
        return self.cursor.fetchall()[0][0]  

    def get_password(self, entry_no):
        # returns an encrypted password
        query = (f"""SELECT password FROM user_entries 
                WHERE entry_no = '{entry_no}'""")
        self.cursor.execute(query)
        output = self.cursor.fetchall()[0][0]
        decrypted_password = self.encryption.decrypt(output, KEY)
        return decrypted_password

    def get_highest_id(self):
        if (self.is_empty()):
            return 0

        query = (f"SELECT MAX(entry_no) FROM user_entries")
        self.cursor.execute(query)
        output = self.cursor.fetchall()[0][0]
        return output
    
    def clear_table(self):
        query = ("DROP TABLE user_entries")   
        self.cursor.execute(query) 
        self.create_table()

    def is_empty(self):
        query = ("SELECT COUNT(*) FROM user_entries")  
        self.cursor.execute(query)
        output = self.cursor.fetchall()[0][0]
        if (output == 0):
            return True
        return False