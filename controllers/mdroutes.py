from bson.json_util import dumps
from flask import Blueprint, make_response, request
import xml.etree.ElementTree as ET
from cerberus import Validator
import requests
import json
# create the blueprint (controller) for the routes
mdroutes = Blueprint('mdroutes', __name__)


def schema_validator(route_id):
    schema = {'route':{'type':'string','maxlength':4}}
    v = Validator(schema)
    input_info = {'route': route_id}
    return v.validate(input_info)

# create GET endpoint to return all routes
@mdroutes.route('/mdroutes/find/all', methods=['GET'])
def show_all_mdroutes():
    try:
        result = requests.get(f'http://www.miamidade.gov/transit/WebServices/BusRoutes/', verify=False)
        # turn result into XML and access root
        root = ET.fromstring(result.text)
        # keys we want
        keys = ['RouteID','RouteAliasLong','RouteColor','Bike','Wheelchair','Airport']
        data = []
        # iterate over all records in root
        for route in root.findall('Record'):
            info = {}
            for key in keys:
                # find tag that matches key and turn into text
                value = route.find(key).text
                if key == 'RouteColor':
                    info[key] = '#'+value
                else:
                    info[key] = value
            # add info to data array
            data.append(info)
    except Exception as e:
        print(e)
        return make_response({'Error': 'Could not fetch data'}, 400)
    # if nothing goes wrong return all of the data and return a 200
    return make_response(json.dumps(data), 200)

@mdroutes.route('/mdroutes/find', methods=['GET'])
def find_mdroute_by_id():
    # parse id param from call
    try:
        route_id = request.args.get('id')
        assert(schema_validator(route_id))
    except Exception as e:
        print(e)
        # return error message and 400 if it throws an exeption
        return make_response({'Error': 'Missing or invalid input'}, 400)
    try:
        result = requests.get(f'http://www.miamidade.gov/transit/WebServices/BusRoutes/?RouteID={route_id}', verify=False)
        # turn result into XML and access root
        root = ET.fromstring(result.text)
        # keys we want
        keys = ['RouteID','RouteAliasLong','RouteColor','Bike','Wheelchair','Airport']
        data = {}
        for route in root.findall('Record'):
            for key in keys:
                # find tag that matches key
                value = route.find(key).text
                if key == 'RouteColor':
                    data[key] = '#'+value
                else:
                    data[key] = value
    except Exception as e:
        print(e)
        # return none and 500 if any errors happen
        return make_response({'Error':'Could not fetch data'}, 400)
    # return json results and send 200
    return make_response(data, 200)
