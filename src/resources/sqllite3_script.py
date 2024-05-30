import sqlite3
import bcrypt 

conn = sqlite3.connect('benutzer.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS benutzer (
        username TEXT PRIMARY KEY NOT NULL,
        password_hash TEXT NOT NULL,
        id INTEGER

    )
    ''')
conn.commit()

def create_password_hash(password):
    passwort_bytes = password.encode('utf-8')
    passwort_hash = bcrypt.hashpw(passwort_bytes, bcrypt.gensalt())
    return passwort_hash


def check_password(password, stored_hash):
    passwort_bytes = password.encode('utf-8')
    return bcrypt.checkpw(passwort_bytes, stored_hash)

def set_user(username, password):
    conn = sqlite3.connect('benutzer.db')
    cursor = conn.cursor()
    password_hash = create_password_hash(password)

    cursor.execute('''
        INSERT INTO benutzer (username, password_hash)
        VALUES (?, ?)
    ''', (username, password_hash))
    conn.commit()


def delete_user(username):
    conn = sqlite3.connect('benutzer.db')
    cursor = conn.cursor()

    cursor.execute('''
        DELETE FROM benutzer
        WHERE username = ?
    ''', (username,))
    conn.commit()
    conn.close()

    
def check_user(username, password):
    conn = sqlite3.connect('benutzer.db')
    cursor = conn.cursor()    
    cursor.execute('''
        SELECT password_hash FROM benutzer
        WHERE username = ?
    ''', (username,))
    
    password_hash = cursor.fetchone()

    if password_hash:
        
        if check_password(password, password_hash[0]):
            print("Login successfully")
            return True
        
        else: 
            print("Wrong password")
            return False 
    else:
        print("Nein")
        return None

def get_users():
    conn = sqlite3.connect('benutzer.db')
    cursor = conn.cursor()
    x = cursor.execute('''
        SELECT * FROM benutzer
        ''')
    
    users = x.fetchall()
    
   
    for user in users:
        print(str(user))
   
    
def is_password_correct(username, password):
    conn = sqlite3.connect('benutzer.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT password_hash FROM benutzer
        WHERE username = ?
    ''', (username,))
    
    password_hash = cursor.fetchone()

    if password_hash:
        if check_password(password, password_hash[0]):
            print("Login successfully")
            conn.close()
            return True
        
        else: 
            print("Wrong password")
            conn.close()
            return False 
        
    else:
        print("Nein")
        conn.close()
        return False
    

conn.close()
