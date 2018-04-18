from flask import Flask
from peewee import PostgresqlDatabase
import os

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = os.urandom(32)
db = PostgresqlDatabase(user=app.config['POSTGRES_USER'],
                        password=app.config['POSTGRES_PASSWORD'],
                        port=app.config['POSTGRES_PORT'],
                        host=app.config['POSTGRES_HOST'],
                        database=app.config['POSTGRES_DB'])

# only import the model once the database connection is configured
from model import *

# import endpoints
import endpoints


@app.cli.command()
def initdb():
    """Initialize the database."""
    print('Preparing database..')
    db.connect()
    db.create_tables([Contribution, Image, Users])
    db.close()
    print('Done!')

@app.before_request
def before_request():
    db.connect(reuse_if_open=True)

@app.after_request
def after_request(response):
    db.close()
    return response
