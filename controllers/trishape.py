from bson.json_util import dumps
from flask import Blueprint, make_response, request
import requests
import json
from cerberus import Validator

# create the blueprint (controller) for the trains
trishape = Blueprint('trishape', __name__)

# schema validator
def schema_validator(route):
    schema = {'route':{'type':'string', 'maxlength':2}}
    v = Validator(schema)
    info = {'route':route}
    return v.validate(info)

def get_coords(stops):
    coords = []
    for stop in stops:
        locations = stop.get('locations', '')
        for location in locations:
            lat = location.get('lat', '')
            lon = location.get('lon', '')
            coords.append([lat, lon])
    return coords

@trishape.route('/trishape/find', methods=['GET'])
def find_trishape():
    try:
        route = request.args.get('id')
        assert(schema_validator(route))
    except:
        return make_response({'Error':'Missing or invalid input'}, 400)

    try:
        # main api call, returns array
        result = requests.get(f'https://transitime-api.goswift.ly/api/v1/key/81YENWXv/agency/trirail/command/tripPatterns?format=json&r={route}')
        # turn request object into text
        data = result.json()
        # get all trips of route
        trips = data.get('tripPatterns', '')
        coords = []
        for trip in trips:
            # get all stops of trip
            stops = trip.get('stopPaths', '')
            info = get_coords(stops)
            # add all coords of trip
            coords += info
    except:
        return make_response({'Error':'Could not fetch data'}, 404)
    # since data is array dump it as string
    return make_response(json.dumps(coords), 200)

