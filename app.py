import os
import sys
from flask import Flask
import auth
import dashboard
import edit_profile
import upload_audio
from utilities import UPLOAD_FOLDER
from rds import RDS_DATABASE

DB_NAME = 'snapcloud.sqlite'

DB_USUARIO = os.getenv("RDS_USUARIO")
DB_SENHA = os.getenv("RDS_SENHA")
RDS_INSTANCIA_ENDPOINT = "database-gabs.cz8e20is81b8.sa-east-1.rds.amazonaws.com"
RDS_INSTANCIA_NOME = "gabs_db"
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USUARIO}:{DB_SENHA}@{RDS_INSTANCIA_ENDPOINT}/{RDS_INSTANCIA_NOME}'



def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(edit_profile.bp)
    app.register_blueprint(upload_audio.bp)

    drop_data_base = True
    RDS_DATABASE.init_app(app)

    try:
        with app.app_context():
            print('Carrega as tabelas do banco')
            if drop_data_base: 
                RDS_DATABASE.drop_all()
                RDS_DATABASE.create_all()
                RDS_DATABASE.session.commit()
        print('Tabelas carregadas com sucesso!')
    except Exception as ex:
        print(f'Erro ao carregar o banco! {str(ex)}')
        sys.exit(1)

    return app