import sys
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from . import app_config as config

# dir_path = os.path.dirname(os.path.realpath(__file__))
# sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))
# from radar_utils import config

global conn
conn = None
last_connection = 0

def create_app():

    dir_path = os.path.dirname(os.path.realpath(__file__))
    # dist_folder = os.path.abspath(os.path.join(dir_path, os.pardir, 'visor_vue2', 'dist'))
    # dist_folder = os.path.abspath(os.path.join(dir_path, 'dist'))

    app = Flask(__name__,
        static_url_path='',
        static_folder='static',
        template_folder='templates')

    app.config.from_object(config.DevelopmentConfig())

    conn.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):

        return User.query.get(int(user_id))

    # Routes Creation
    from .routes_api import blueprint as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    from .routes_auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .routes_main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    @app.after_request
    def after_request(response):
        header = response.headers
        header['Access-Control-Allow-Origin'] = '*'
        return response

    return app

def reconnect():
    global conn
    conn = SQLAlchemy()
    return conn

conn = reconnect()