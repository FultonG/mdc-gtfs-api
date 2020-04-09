from bson.json_util import dumps
from flask import Blueprint, make_response, request
import xml.etree.ElementTree as ET
from cerberus import Validator
import requests
import json
# create the blueprint (controller) for the routes
mdstations = Blueprint('mdstations', __name__)

def schema_validator(station_id):
    schema = {'station':{'type':'string','maxlength':3}}
    v = Validator(schema)
    input_info = {'station': station_id}
    return v.validate(input_info)

@mdstations.route('/mdstations/find/all', methods=['GET'])
def find_mdstations_all():
    try:
        result = requests.get(f'http://www.miamidade.gov/transit/WebServices/TrainStations/', verify=False)
        # turn result into xml and access root
        root = ET.fromstring(result.text)
        keys = ['StationID','Station','Address','City','State','Zip','Airport','TriRail','Location']
        data = []
        # iterate over all records in root
        for station in root.findall('Record'):
            info = {}
            for key in keys:
                if key == 'Location':
                    lat = station.find('Latitude').text
                    lon = station.find('Longitude').text
                    info[key] = [lat, lon]
                else:
                    value = station.find(key).text
                    info[key] = value
            data.append(info)
    except Exception as e:
        print(e)
        # return none and 500 if any errors happen
        return make_response({'Error':'Could not fetch data'}, 400)
    # return json results and send 200
    return make_response(json.dumps(data), 200)

@mdstations.route('/mdstations/find', methods=['GET'])
def find_mdstations():
    # parse id param from call
    try:
        station_id = request.args.get('station_id')
        assert(schema_validator(station_id))
    except Exception as e:
        print(e)
        # return error message and 400 if it throws an exeption
        return make_response({'Error': 'Missing or invalid input'}, 400)
    try:
        result = requests.get(f'http://www.miamidade.gov/transit/WebServices/TrainStations/?StationID={station_id}', verify=False)
        # turn result into xml and access root
        root = ET.fromstring(result.text)
        keys = ['StationID','Station','Address','City','State','Zip','Airport','TriRail','Location']
        data = {}
        # iterate over all records in root
        for station in root.findall('Record'):
            for key in keys:
                if key == 'Location':
                    lat = station.find('Latitude').text
                    lon = station.find('Longitude').text
                    data[key] = [lat, lon]
                else:
                    value = station.find(key).text
                    data[key] = value
    except Exception as e:
        print(e)
        # return none and 500 if any errors happen
        return make_response({'Error':'Could not fetch data'}, 400)
    # return json results and send 200
    return make_response(data, 200)
