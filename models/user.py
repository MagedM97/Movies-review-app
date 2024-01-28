from database import mysql
from werkzeug.security import check_password_hash,generate_password_hash

# User class for handling user authentication
class User:
    def __init__(self, id, username, email, isAdmin):
        self.id = id
        self.username = username
        self.email = email
        self.isAdmin = isAdmin

    @staticmethod
    def find_by_email_and_password(email, password):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user_data = cur.fetchone()
        cur.close()

        if user_data and check_password_hash(user_data[3], password):
            return User(user_data[0], user_data[1], user_data[2], user_data[4])
        else:
            return None
    
    @staticmethod
    def register(username, email, password):
        cur = mysql.connection.cursor()   
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        if user:
            return False, "Email already exists. Please use a different email."    
        password_hash = generate_password_hash(password)
        cur.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password_hash, email))
        mysql.connection.commit()    
        cur.close()
        return True, "Successful Registration"