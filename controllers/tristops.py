from bson.json_util import dumps
from flask import Blueprint, make_response, request
import requests
import json
from cerberus import Validator

# create the blueprint (controller) for the trains
tristops = Blueprint('tristops', __name__)

# schema validator
def schema_validator(route):
    schema = {'route':{'type':'string', 'maxlength':2}}
    v = Validator(schema)
    info = {'route':route}
    return v.validate(info)

@tristops.route('/tristops/find', methods=['GET'])
def find_tristops():
    try:
        route = request.args.get('id')
        assert(schema_validator(route))
    except:
        return make_response({'Error':'Missing or invalid input'}, 400)

    try:
        # main api call, returns array
        result = requests.get(f'https://transitime-api.goswift.ly/api/v1/key/81YENWXv/agency/trirail/command/stops?format=json&r={route}')
        # turn request object into text
        result_json = result.json()
        # data we want is only in first index
        directions = result_json.get('directions', ' ')[0]
        # stop key that holds all stops as value
        stops = directions.get('stops', ' ')
        data = []
        for stop in stops:
            info = {}
            lat = stop.get('lat', '')
            lon = stop.get('lon', '')
            info['name'] = stop.get('name', '')
            info['shape'] = [lat, lon]
            data.append(info)
    except:
        return make_response({'Error':'Could not fetch data'}, 404)
    # since data is array dump it as string
    return make_response(json.dumps(data), 200)

