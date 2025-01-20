import os
import sys
from flask import Flask
import auth
import dashboard
import edit_profile
from rds import RDS_DATABASE

DB_NAME = 'snapcloud.sqlite'

DB_USUARIO = "admin"
DB_SENHA = "*djbFvNS83]d?"
RDS_INSTANCIA_ENDPOINT = "snapcloud-database-1.cz8e20is81b8.sa-east-1.rds.amazonaws.com"
RDS_INSTANCIA_NOME = "snapcloud-database-1"
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USUARIO}:{DB_SENHA}@{RDS_INSTANCIA_ENDPOINT}/{RDS_INSTANCIA_NOME}'



def create_app():
    app = Flask(__name__)
    app.secret_key = '3db0afb59439b1c95c3262cb1daf63ea0d3f2a31180f072371559c882e82ad7a'
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(edit_profile.bp)

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