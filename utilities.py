import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
DB_NAME = "snapcloud.db"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_folders():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

def create_tables():
    with open("schema.sql", "r") as file:
        schema = file.read()
        conn = sqlite3.connect(DB_NAME)
        conn.executescript(schema)