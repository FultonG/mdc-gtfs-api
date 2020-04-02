from bson.json_util import dumps
from flask import Blueprint, make_response, request
import requests
import json

stations = Blueprint('stations', __name__)

@stations.route('/stations', methods=['GET'])
def send_stations():
    # every acceptable station and its location
    stations = {'Miami':'MIA','West Palm Beach':'PBI','Fort Lauderdale':'FLL'}
    return make_response(dumps(stations), 200)

