from bson.json_util import dumps
from flask import Blueprint, make_response, request
import xml.etree.ElementTree as ET
from cerberus import Validator
import requests
import json
# create the blueprint (controller) for the routes
mdtrain = Blueprint('mdtrain', __name__)

def schema_validator(train_id):
    schema = {'train':{'type':'string','maxlength':3}}
    v = Validator(schema)
    input_info = {'train': train_id}
    return v.validate(input_info)

# create GET endpoint to return all routes
@mdtrain.route('/mdtrain/find/all', methods=['GET'])
def show_all_mdtrain():
    try:
        result = requests.get(f'http://www.miamidade.gov/transit/WebServices/Trains/', verify=False)
        # turn result into XML and access root
        root = ET.fromstring(result.text)
        # keys we want
        keys = ['TrainID','LineID','Coords','ServiceDirection','Service','LocationUpdated']
        data = []
        # iterate over all records in root
        for train in root.findall('Record'):
            info = {}
            for key in keys:
                # if key is Coords add lat and lon to info as array
                if key == 'Coords':
                    lat = train.find('Latitude').text
                    lon = train.find('Longitude').text
                    info[key] = [lat, lon]
                else:
                    # find tag that matches key and turn into text
                    value = train.find(key).text
                    info[key] = value
            # add info to data array
            data.append(info)
    except Exception as e:
        print(e)
        return make_response({'Error': 'Could not fetch data'}, 400)
    # if nothing goes wrong return all of the data and return a 200
    return make_response(json.dumps(data), 200)

@mdtrain.route('/mdtrain/find', methods=['GET'])
def find_mdtrain_by_id():
    # parse id param from call
    try:
        train_id = request.args.get('id')
        assert(schema_validator(train_id))
    except Exception as e:
        print(e)
        # return error message and 400 if it throws an exeption
        return make_response({'Error': 'Missing or invalid input'}, 400)
    try:
        result = requests.get(f'http://www.miamidade.gov/transit/WebServices/Trains/?TrainID={train_id}', verify=False)
        # turn result into XML and access root
        root = ET.fromstring(result.text)
        # keys we want
        keys = ['TrainID','LineID','Coords','ServiceDirection','Service','LocationUpdated']
        data = {}
        for train in root.findall('Record'):
            for key in keys:
                # if key is Coords add lat and lon to info as array
                if key == 'Coords':
                    lat = train.find('Latitude').text
                    lon = train.find('Longitude').text
                    data[key] = [lat, lon]
                else:
                    # find tag that matches key and turn into text
                    value = train.find(key).text
                    data[key] = value
    except Exception as e:
        print(e)
        # return none and 500 if any errors happen
        return make_response({'Error':'Could not fetch data'}, 400)
    # return json results and send 200
    return make_response(data, 200)
