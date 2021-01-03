import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))
# from radar_utils import config

# CONNECTION = config.CONNECTION_DATABASE['PRODUCTION']


class Config(object):
    # Statement for enabling the development environment
    DEBUG = True
    FLASK_APP = 'api'

    # Define the application directory
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

    # Define the database - we are working with
    # SQLite for this example
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
    # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{CONNECTION['user']}:{CONNECTION['password']}@{CONNECTION['host']}:{CONNECTION['port']}/{CONNECTION['database']}?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_recycle': 300,
    }
    DATABASE_CONNECT_OPTIONS = {}

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2

    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    CSRF_ENABLED     = True

    # Use a secure, unique and absolutely secret key for
    # signing the data. 
    CSRF_SESSION_KEY = "ia0J7+lkdRiQosep"

    # Secret key for signing cookies
    SECRET_KEY = "jMPh0ic8cQ4m95ty"

class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False
    #DB_HOST = 'localhost'

class DevelopmentConfig(Config):
    SESSION_COOKIE_SECURE = False
