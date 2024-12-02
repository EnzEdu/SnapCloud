import os
from flask import Flask
import auth
import dashboard
import edit_profile
from utilities import UPLOAD_FOLDER

DB_NAME = 'snapcloud.sqlite'

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(edit_profile.bp)
    
    return app