import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
DB_NAME = "snapcloud.db"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS