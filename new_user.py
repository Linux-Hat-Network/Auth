import sqlite3
import bcrypt

db = sqlite3.connect("instance/database.db")
cursor = db.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS "Users" ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT, password_salt TEXT, is_admin INTEGER);''')
db.commit()

def new_user():
    name = input("username: ")
    cursor.execute("SELECT name FROM Users WHERE name = ?", (name,))
    
    if cursor.fetchone():
        print("User already exists")
        return
    
    password = input("password: ")
    
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    is_admin = int(input("is admin (0 or 1): "))
    if is_admin not in [0, 1]:
        print("Invalid input for is_admin. Must be 0 or 1.")
        return
    
    cursor.execute(
        "INSERT INTO Users (name, password, password_salt, is_admin) VALUES (?, ?, ?, ?)", (name, hash, salt, is_admin))
    db.commit()
    
    print(f"User {name} has been added")

new_user()