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
        print(result.url)
        result_json = result.json()
        routes = result_json.get('get_routes', '')
        keys = {'id', 'name', 'abbr', 'stops', 'vType', 'encLine', 'color'}
        data = []
        for route in routes:
            info = {}
            for key in keys:
                if key == 'encLine':
                    encoded_polyline = route.get(key, '')
                    info['shape'] = polyline.decode(encoded_polyline)
                else:
                    info[key] = route.get(key, '')
            data.append(info)
    except Exception as e:
        print(e)
        return make_response({'Error':'Could not fetch data'}, 500)
    return make_response(json.dumps(data), 200)

@trolley.route('/trolley/find', methods=['GET'])
def find_trolley():
    try:
        route = request.args.get('id')
        assert(schema_validator(route))
    except:
        return make_response({'Error':'Missing or invalid input'}, 500)

    try:
        # main api call, returns array
        result = requests.get(f'http://cgpublic.etaspot.net/service.php?service=get_routes&routeID={route}&token=TESTING', verify=False)
        result_json = result.json()
        route = result_json.get('get_routes', ' ')[0]
        keys = ['id', 'name', 'abbr', 'stops', 'vType', 'encLine', 'color']
        info = {}
        for key in keys:
            if key == 'encLine':
                encoded_polyline = route.get(key, '')
                info['shape'] = polyline.decode(encoded_polyline)
            else:
                info[key] = route.get(key, '')
        route = info
    except Exception as e:
        print(e)
        return make_response({'Error':'Could not fetch data'}, 500)
    # since data is array dump it as string
    return make_response(json.dumps(route), 200)


