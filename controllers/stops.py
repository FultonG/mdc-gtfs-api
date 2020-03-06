from bson.json_util import dumps
from flask import Blueprint, make_response, request
from .instances import mongo
import requests
import json
import polyline

stops = Blueprint('stops', __name__)

# endpoint to get all shapes
@stops.route('/stops/find', methods=['GET'])
def find_stops_by_id():
    # parse id param from call
    try:
        route_id = request.args.get('id')
    except:
        # return error message and 400 if it throws an exeption
        return make_response({'Error':'Missing or invalid input'}, 400)
    # call enpoint with token and route
    try:
        result = requests.get('https://rest.tsoapi.com/PubTrans/GetModuleInfoPublic?Key=ROUTE_STOPS_AND_UNITS&id={}&lan=en'.format(route_id), verify=False)
        # turn result into json
        result_json = result.json()
        data = json.loads(result_json)
        # only usefull info in our data is in the 0 index
        stops_data = data[0]
        # create variable to hold all the stops
        all_stops = []
        # loop over every dictionary in stops_data to get lat and lon
        for stop_info in stops_data:
            lat = int(stop_info['Latitude'])
            lon = int(stop_info['Longitude'])
            all_stops.append([lat, lon])
    # raise error if exception
    except Exception as e:
        print(e)
        return make_response({}, 500)
    # return data_info
    return make_response(dumps(all_stops), 200)

