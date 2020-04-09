from bson.json_util import dumps
from flask import Blueprint, make_response, request
import requests
import json
import polyline

stops = Blueprint('stops', __name__)

def schema_validator(route):
    schema = {'route':{'type':'string','maxlength':10}}
    v = Validator(schema)
    input_info = {'route':route}
    return v.validate(input_info)

# endpoint to get all shapes
@stops.route('/stops/find', methods=['GET'])
def find_stops_by_id():
    # parse id param from call
    try:
        route_id = request.args.get('id')
    except Exception as e:
        print(e)
        # return error message and 400 if it throws an exeption
        return make_response({'Error':'Missing or invalid input'}, 400)
    # call enpoint with token and route
    try:
        result = requests.get(f'https://rest.tsoapi.com/PubTrans/GetModuleInfoPublic?key=route_stops&id={route_id}', verify=False)
        # turn result into json
        result_json = result.json()
        data = json.loads(result_json)
        # create variable to hold all the stops
        all_stops = []
        # loop over every dictionary in stops_data to get lat and lon
        for stop_info in data:
            info = {}
            lat = float(stop_info['Latitude'])
            lon = float(stop_info['Longitude'])
            info['Shape'] = [lat, lon]
            info['Street'] = stop_info['Street']
            info['StopName'] = stop_info['StopName']
            all_stops.append(info)
    # raise error if exception
    except Exception as e:
        print(e)
        return make_response({'Error':'Could not fetch data'}, 400)
    # return data_info
    return make_response(dumps(all_stops), 200)

