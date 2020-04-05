from bson.json_util import dumps
from flask import Blueprint, make_response, request
import requests
import json
from cerberus import Validator

# create the blueprint (controller) for the trains
trirail = Blueprint('trirail', __name__)

# schema validator
def schema_validator(route):
    schema = {'route':{'type':'string', 'maxlength':2}}
    v = Validator(schema)
    info = {'route':route}
    return v.validate(info)

@trirail.route('/trirail/find/all', methods=['GET'])
def find_trirail_all():
    try:
        result = requests.get(f'https://transitime-api.goswift.ly/api/v1/key/81YENWXv/agency/trirail/command/routes?format=json')
        result_json = result.json()
        data = result_json.get('routes', '')
        for route in data:
            # add '#' to color string to make frontend happy
            route['color'] = '#'+route['color']
            # delete useless info
            del route['type']
    except:
        return make_response({'Error':'Could not load data'}, 404)
    return make_response(json.dumps(data), 200)

@trirail.route('/trirail/find', methods=['GET'])
def find_trirail():
    try:
        route = request.args.get('id')
        assert(schema_validator(route))
    except:
        return make_response({'Error':'Missing or invalid input'}, 404)

    try:
        # main api call, returns array
        result = requests.get(f'https://transitime-api.goswift.ly/api/v1/key/81YENWXv/agency/trirail/command/routes?format=json&r={route}')
        # turn request object into text
        result_json = result.json()
        data = result_json.get('routes', ' ')[0]
        # add '#' to color string to make frontend happy
        data['color'] = '#'+data['color']
        # delete useless info
        del data['type']
    except:
        return make_response({'Error':'Could not fetch data'}, 404)
    # since data is array dump it as string
    return make_response(json.dumps(data), 200)

