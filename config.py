import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    # The idea is that a value sourced from an environment variable is preferred, but if the environment does not define the variable,
    # then the hardcoded string is used instead. When you are developing this application, 
    # the security requirements are low, so you can just ignore this setting and let the hardcoded string be used. But when this application 
    # is deployed on a production server, I will be setting a unique and difficult to guess value in the environment, so that the server has 
    # a secure key that nobody else knows.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'teachersRock!'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']
    POSTS_PER_PAGE = 25
    
