from bson.json_util import dumps
from flask import Blueprint, make_response, request
import xml.etree.ElementTree as ET
from cerberus import Validator
import requests
import json
# create the blueprint (controller) for the routes
mdbus = Blueprint('mdbus', __name__)

def schema_validator(route_id):
    schema = {'route':{'type':'string','maxlength':4}}
    v = Validator(schema)
    input_info = {'route': route_id}
    return v.validate(input_info)

# create GET endpoint to return all routes
@mdbus.route('/mdbus/find/all', methods=['GET'])
def show_all_mdbus():
    try:
        result = requests.get(f'http://www.miamidade.gov/transit/WebServices/Buses/', verify=False)
        # turn result into XML and access root
        root = ET.fromstring(result.text)
        # keys we need
        keys = ['BusID','BusName','Coords','RouteID','TripID','LocationUpdated','TripHeadsign']
        data = []
        for bus in root.findall('Record'):
            info = {}
            for key in keys:
                # if key is coord get lat and lon from bus
                if key == 'Coords':
                    lat = bus.find('Latitude').text
                    lon = bus.find('Longitude').text
                    info[key] = [lat, lon]
                # find tag that matches key
                else:
                    value = bus.find(key).text
                    info[key] = value
            # add info to data
            data.append(info)
    except Exception as e:
        print(e)
        return make_response({'Error': 'Could not fetch data'}, 400)
    # if nothing goes wrong return all of the data and return a 200
    return make_response(json.dumps(data), 200)

@mdbus.route('/mdbus/find', methods=['GET'])
def find_mdbus_by_id():
    # parse id param from call
    try:
        bus_id = request.args.get('id')
        assert(schema_validator(bus_id))
    except Exception as e:
        print(e)
        # return error message and 400 if it throws an exeption
        return make_response({'Error': 'Missing or invalid input'}, 400)
    try:
        result = requests.get(f'http://www.miamidade.gov/transit/WebServices/Buses/?BusID={bus_id}', verify=False)
        # turn result into XML and access root
        root = ET.fromstring(result.text)
        # keys we need
        keys = ['BusID','BusName','Coords','RouteID','TripID','LocationUpdated','TripHeadsign']
        data = {}
        for bus in root.findall('Record'):
            for key in keys:
                # if key is coords get lat and lon from bus
                if key == 'Coords':
                    lat = bus.find('Latitude').text
                    lon = bus.find('Longitude').text
                    # add info to data dictionary
                    data[key] = [lat, lon]
                # find tag that matches key
                else:
                    value = bus.find(key).text
                    # add info to data dictionary
                    data[key] = value
    except Exception as e:
        print(e)
        # return none and 500 if any errors happen
        return make_response({'Error':'Could not fetch data'}, 400)
    # return json results and send 200
    return make_response(data, 200)
