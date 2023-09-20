import sqlite3
from sqlite3 import OperationalError
import os

class ManageUser:
    """This class is used to manage users."""

    def __init__(self, database_file): #copypasta van tablemodel.py, don't reinvent the wheel.
        self.database_file = database_file
        if not os.path.exists(self.database_file):
            raise FileNotFoundError(f"Could not find database file: {database_file}")

    #add new user
    def add_new_user(self, username, password, admin): #copypasta van demodatabase.py
        try:
            connection = sqlite3.connect(self.database_file)
            cursor = connection.cursor()
        
            #SQL statement to insert new user, didn't pass along the id bc it's on auto-increment anyways.
            new_user_qry = "INSERT INTO users (gebruikersnaam, wachtwoord, is_admin) VALUES (?, ?, ?)"
            new_user = (username, password, admin)
        
            cursor.execute(new_user_qry, new_user)
            connection.commit()

            connection.close()

        except OperationalError as e:
            print(f"Error opening database file {self.database_file}")
            raise e 
        
    def edit_user(self, username, password, admin, id):
        try:
            connection = sqlite3.connect(self.database_file)
            cursor = connection.cursor()
        
            #SQL statement to update an existing user
            update_user_qry = "UPDATE users SET gebruikersnaam = ?, wachtwoord = ?, is_admin = ? WHERE user_id = ?"
            edit_user = (username, password, admin, id)

            cursor.execute(update_user_qry, edit_user)
            connection.commit()

            connection.close()

        except OperationalError as e:
            print(f"Error opening database file {self.database_file}")
            raise e

    def login_user(self, username, password):
        try:
            connection = sqlite3.connect(self.database_file)
            cursor = connection.cursor()
        
            #SQL statement to check if user is present in db
            check_user_qry = "SELECT * FROM users WHERE gebruikersnaam = ? AND wachtwoord = ?"
            login_user = (username, password)

            cursor.execute(check_user_qry, login_user)
            user = cursor.fetchone() #fetchall geeft alle matchende rows terug, fetchone alleen één row of none als t er niet is. 
            connection.commit()

            connection.close()

        except OperationalError as e:
            print(f"Error opening database file {self.database_file}")
            raise e 
        return user

    def get_user(self, id):
        try:
            connection = sqlite3.connect(self.database_file)
            cursor = connection.cursor()
        
            #SQL statement to get user from table
            get_user_qry = "SELECT * FROM users WHERE user_id = ?"

            cursor.execute(get_user_qry, [id]) #ik weet niet waarom hij zonder de brackets brak maar oké, sure
            user = cursor.fetchone() 
            connection.commit()

            connection.close()

        except OperationalError as e:
            print(f"Error opening database file {self.database_file}")
            raise e 
        return user
    
    def delete_user(self, id):
        try:
            connection = sqlite3.connect(self.database_file)
            cursor = connection.cursor()
        
            #SQL statement to delete an existing user
            delete_user_qry = "DELETE FROM users WHERE user_id = ?"

            #need to reset sqlite_sequence table bc user_id = autoincrement
            reset_seq_qry = "UPDATE 'sqlite_sequence' SET 'seq' = (SELECT MAX('user_id') FROM 'users') WHERE 'name' = 'users'"
            
            cursor.execute(delete_user_qry, [id])
            connection.commit()

            cursor.execute(reset_seq_qry)
            connection.commit()

            connection.close()

        except OperationalError as e:
            print(f"Error opening database file {self.database_file}")
            raise e
        