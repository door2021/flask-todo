from datetime import timedelta
import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or "TodosAppSecretKeyDev"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Email Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') != 'False'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/todos"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.environ.get('RDS_USERNAME')}:"
        f"{os.environ.get('RDS_PASSWORD')}@"
        f"{os.environ.get('RDS_HOSTNAME')}:"
        f"{os.environ.get('RDS_PORT')}/"
        f"{os.environ.get('RDS_DB_NAME')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'TodosAppSecretKeyDev')
    WTF_CSRF_ENABLED = os.environ.get('WTF_CSRF_ENABLED', 'True') == 'True'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/todos"
    SQLALCHEMY_TRACK_MODIFICATIONS = False