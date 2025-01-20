import os
from flask import Flask
import auth
import dashboard
import edit_profile
from utilities import UPLOAD_FOLDER

DB_NAME = 'snapcloud.sqlite'

DB_USUARIO = os.getenv('RDS_USUARIO')
DB_SENHA = os.getenv('RDS_SENHA')
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
    
    return app