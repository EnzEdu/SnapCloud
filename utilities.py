import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
DB_NAME = "snapcloud.db"

def create_tables():
    with open("schema.sql", "r") as file:
        schema = file.read()
        conn = sqlite3.connect(DB_NAME)
        conn.executescript(schema)

def create_a_user():
    full_name = "Joao da Silva"
    username = "joao"
    password = "12345678"
    email = "joao@mail.com"
    description = "I like to post photographies, listen to music and watch videos!"
    creation_date = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
    profile_picture = "static/default-placeholder.jpg"

    hashed_password = generate_password_hash(password)

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO USERS (full_name, username, password, email, description, creation_date, profile_picture) VALUES (?, ?, ?, ?, ?, ?, ?)", (full_name, username, hashed_password, email, description, creation_date, profile_picture))
        conn.commit()
        conn.close()
    
    except sqlite3.IntegrityError as e:
        print(e)

def update_a_user():
    username = "joao"
    password = "12345678"
    hashed_password = generate_password_hash(password)

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE USERS SET PASSWORD = ? WHERE USERNAME = ?", (hashed_password, username,))
        conn.commit()
        conn.close()
    
    except sqlite3.IntegrityError as e:
        print(e)

def get_a_user():
    username = "joao"
    password = "12345678"

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    user = cursor.execute("select * from users where username = ?", (username,)).fetchone()
    conn.close()

    return user