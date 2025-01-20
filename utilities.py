import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

from flask_sqlalchemy import SQLAlchemy
import sys

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
DB_NAME = "snapcloud.db"

# Instancia o componente de banco de dados
RDS_DATABASE = SQLAlchemy()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_folders():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

class Usuario(RDS_DATABASE.Model):
    id = RDS_DATABASE.Column(RDS_DATABASE.Integer, primary_key=True)
    full_name = RDS_DATABASE.Column(RDS_DATABASE.String(100))
    username = RDS_DATABASE.Column(RDS_DATABASE.String(100))
    password = RDS_DATABASE.Column(RDS_DATABASE.String(25))
    email = RDS_DATABASE.Column(RDS_DATABASE.String(100))
    description = RDS_DATABASE.Column(RDS_DATABASE.String(256))
    creation_date = RDS_DATABASE.Column(RDS_DATABASE.Time(True))
    profile_picture = RDS_DATABASE.Column(RDS_DATABASE.String(100))

def create_tables(app, drop_data_base):
    RDS_DATABASE.init_app(app)

    try:
        with app.app_context():
            print('Carrega as tabelas do banco')
            if (drop_data_base):
                RDS_DATABASE.drop_all()
                RDS_DATABASE.create_all()
                RDS_DATABASE.session.commit()
            print('Tabelas carregadas com sucesso!')
    except Exception as ex:
        print(f'Erro ao carregar o banco! {str(ex)}')
        sys.exit(1)