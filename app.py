import os
from flask import Flask
import auth
import dashboard
import user_settings

DB_NAME = 'snapcloud.sqlite'

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    try:
        os.makedirs(app.instance_path)

    except OSError:
        pass

    
    app.register_blueprint(auth.bp)
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(user_settings.bp)
    
    return app