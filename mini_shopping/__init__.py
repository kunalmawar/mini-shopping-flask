#!flask/bin/python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


POSTGRES = {
    'user': 'kunal',
    'pw': '',
    'db': 'mini_shopping',
    'host': 'localhost',
    'port': '5432',
}

app = Flask(__name__)

# Configs
settings = {
    'DEBUG': True,
    'SQLALCHEMY_DATABASE_URI': 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES,
    'TEMPLATES_AUTO_RELOAD': True,
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SECRET_KEY': 'd44b6693-5e35-4a88-9a11-f80b14a281b7'
}
app.config.update(settings)

# DB instance
db = SQLAlchemy(app)

from mini_shopping import routes
from mini_shopping import auth
from mini_shopping import api
app.register_blueprint(auth.bp)
app.register_blueprint(api.bp)