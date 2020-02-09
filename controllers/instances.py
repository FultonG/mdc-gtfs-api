import os
import json
import os.path
from flask import Flask
from flask_pymongo import PyMongo

# start flask instance
app = Flask(__name__)

# set filename for the environments path
SECRETS_pathname = 'SECRET_KEYS.json'

# check if file exists, if not, assume it's in a config var
if os.path.isfile(SECRETS_pathname):
    with open(SECRETS_pathname) as f:
        MONGO_URI = json.load(f)['MONGO_URI']
else:
    MONGO_URI = os.environ['MONGO_URI']

# set flask instance config variable for the database
app.config['MONGO_URI'] = MONGO_URI
# instanciate the mongo client using the app's env vars
mongo = PyMongo()

# now that everything is instanciated, initialize mongo client
mongo.init_app(app)
