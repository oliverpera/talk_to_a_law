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
    password_hash = create_password_hash(password)

    cursor.execute('''
        INSERT INTO benutzer (username, password_hash)
        VALUES (?, ?)
    ''', (username, password_hash))
    conn.commit()
    
def check_user(username, password):    
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
    x = cursor.execute('''
        SELECT * FROM benutzer
        ''')
    
    users = x.fetchall()
    
   
    for user in users:
        print(str(user))
   
    
    
    
# set_user('Hellstern', 'Hellstern_ist_toll')
# set_user('Olli', 'Olli_ist_toll')
# set_user('Robin', 'Robin_ist_toll')
# set_user('Timon', 'Timon_ist_toll')

# get_users()
check_user('Olli', 'Olli_ist_toll')
# check_user('Timon', 'Timon_ist_toll')




print(cursor.execute('''
        SELECT username FROM benutzer
        WHERE username = ?
    ''', ("Olli",)).fetchone())



conn.close()
