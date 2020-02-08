import json
from flask import Flask
from flask_pymongo import PyMongo

# start flask instance
app = Flask(__name__)

# read mongo uri from secret file
SECRETS_pathname = 'SECRET_KEYS.json'
with open(SECRETS_pathname) as f:
    MONGO_URI = json.load(f)['MONGO_URI']

# set flask instance config variable for the database
app.config['MONGO_URI'] = MONGO_URI
# instanciate the mongo client using the app's env vars
mongo = PyMongo()

# now that everything is instanciated, initialize mongo client
mongo.init_app(app)
