from bson.json_util import dumps
from flask import Blueprint, make_response, request
from cerberus import Validator
import requests
import json
import polyline

trostops = Blueprint('trostops', __name__)

# schema validator
def schema_validator(route):
    schema = {'route':{'type':'string', 'maxlength':1}}
    v = Validator(schema)
    info = {'route':route}
    return v.validate(info)

@trostops.route('/trostops/find', methods=['GET'])
def find_trostops():
    try:
        route = request.args.get('id')
        assert(schema_validator(route))
    except:
        return make_response({'Error':'Missing or invalid input'}, 400)

    try:
        # main api call, returns array
        result = requests.get(f'http://cgpublic.etaspot.net/service.php?service=get_stops&routeID={route}&token=TESTING', verify=False)
        result_json = result.json()
        stops = result_json.get('get_stops', ' ')
        data = []
        for stop in stops:
            info = {}
            lat = stop.get('lat', '')
            lon = stop.get('lng', '')
            info['shape'] = [lat, lon]
            info['address'] = stop.get('name', '')
            data.append(info)
    except Exception as e:
        print(e)
        return make_response({'Error':'Could not fetch data'}, 400)
    # since data is array dump it as string
    return make_response(json.dumps(data), 200)


