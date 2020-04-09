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
    except Exception as e:
        print(e)
        return make_response({'Error':'Missing or invalid input'}, 400)

    try:
        # main api call
        result = requests.get(f'http://cgpublic.etaspot.net/service.php?service=get_stops&routeID={route}&token=TESTING', verify=False)
        result_json = result.json()
        # key that holds all stops in array
        stops = result_json.get('get_stops', ' ')
        # variable that will hold our stops
        data = []
        for stop in stops:
            info = {}
            # get lat from stop
            lat = stop.get('lat', '')
            # get lon from stop
            lon = stop.get('lng', '')
            # put lat and lon in array
            info['shape'] = [lat, lon]
            # get street name of stop
            info['address'] = stop.get('name', '')
            # add the info to our data
            data.append(info)
    except Exception as e:
        print(e)
        return make_response({'Error':'Could not fetch data'}, 400)
    # since data is array dump it as string
    return make_response(json.dumps(data), 200)
