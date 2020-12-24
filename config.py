import os


class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://{}:{}@localhost/flaskdb".format(
        os.getenv("POSTGRES_USER"), os.getenv("POSTGRES_PASSWORD")
    )
    SECRET_KEY = "some secret key"
