import os
from flask import Flask
import auth
import dashboard
import edit_profile
from utilities import UPLOAD_FOLDER

DB_NAME = 'snapcloud.sqlite'

def create_app():
    app = Flask(__name__)
    app.secret_key = '3db0afb59439b1c95c3262cb1daf63ea0d3f2a31180f072371559c882e82ad7a'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(edit_profile.bp)
    
    return app