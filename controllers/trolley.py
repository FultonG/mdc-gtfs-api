from bson.json_util import dumps
from flask import Blueprint, make_response, request
from cerberus import Validator
import requests
import json
import polyline

trolley = Blueprint('trolley', __name__)

# schema validator
def schema_validator(route):
    schema = {'route':{'type':'string', 'maxlength':1}}
    v = Validator(schema)
    info = {'route':route}
    return v.validate(info)

@trolley.route('/trolley/find/all', methods=['GET'])
def find_trolley_all():
    try:
        result = requests.get('http://cgpublic.etaspot.net/service.php?service=get_routes&token=TESTING', verify=False)
        result_json = result.json()
        # access key that hold all routes
        routes = result_json.get('get_routes', '')
        # keys that we need
        keys = {'id', 'name', 'abbr', 'stops', 'vType', 'encLine', 'color'}
        # variable to hold our data
        data = []
        for route in routes:
            info = {}
            for key in keys:
                # if key is 'encLine' polyline decode it
                if key == 'encLine':
                    encoded_polyline = route.get(key, '')
                    info['shape'] = polyline.decode(encoded_polyline)
                # get key from route
                else:
                    info[key] = route.get(key, '')
            # add out info to data
            data.append(info)
    except Exception as e:
        print(e)
        return make_response({'Error':'Could not fetch data'}, 400)
    return make_response(json.dumps(data), 200)

@trolley.route('/trolley/find', methods=['GET'])
def find_trolley():
    try:
        route = request.args.get('id')
        assert(schema_validator(route))
    except Exception as e:
        print(e)
        return make_response({'Error':'Missing or invalid input'}, 400)

    try:
        # main api call
        result = requests.get(f'http://cgpublic.etaspot.net/service.php?service=get_routes&routeID={route}&token=TESTING', verify=False)
        result_json = result.json()
        # only one route so index at 0
        route = result_json.get('get_routes', ' ')[0]
        # keys that we need
        keys = ['id', 'name', 'abbr', 'stops', 'vType', 'encLine', 'color']
        info = {}
        for key in keys:
            # if key is 'encLine' polyline decode it and add to info
            if key == 'encLine':
                encoded_polyline = route.get(key, '')
                info['shape'] = polyline.decode(encoded_polyline)
            # add key value to info
            else:
                info[key] = route.get(key, '')
        # replace route with info of data we need
        route = info
    except Exception as e:
        print(e)
        return make_response({'Error':'Could not fetch data'}, 400)
    # since data is array dump it as string
    return make_response(json.dumps(route), 200)


