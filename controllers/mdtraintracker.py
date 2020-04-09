from bson.json_util import dumps
from flask import Blueprint, make_response, request
import xml.etree.ElementTree as ET
from cerberus import Validator
import requests
import json
# create the blueprint (controller) for the routes
mdtraintracker = Blueprint('mdtraintracker', __name__)

def schema_validator(station_id):
    schema = {'station':{'type':'string','maxlength':3}}
    v = Validator(schema)
    input_info = {'station': station_id}
    return v.validate(input_info)

@mdtraintracker.route('/mdtraintracker/find', methods=['GET'])
def find_mdtraintracker():
    # parse id param from call
    try:
        station_id = request.args.get('station_id')
        assert(schema_validator(station_id))
    except Exception as e:
        print(e)
        # return error message and 400 if it throws an exeption
        return make_response({'Error': 'Missing or invalid input'}, 400)
    try:
        result = requests.get(f'http://www.miamidade.gov/transit/WebServices/TrainTracker/?StationID={station_id}', verify=False)
        # turn result into xml and access root
        root = ET.fromstring(result.text)
        keys = ['StationID','StationName','NB_Time1','NB_Time1_Arrival','NB_Time1_Train','NB_Time1_LineID','NB_Time2','NB_Time2_Arrival','NB_Time2_Train','NB_Time2_LineID','NB_Time3','NB_Time3_Arrival','NB_Time3_Train','NB_Time3_LineID','SB_Time1','SB_Time1_Arrival','SB_Time1_Train','SB_Time1_LineID','SB_Time2','SB_Time2_Arrival','SB_Time2_Train','SB_Time2_LineID','SB_Time3','SB_Time3_Arrival','SB_Time3_Train','SB_Time3_LineID']
        data = {}
        # iterate over all records in root
        for station in root.findall('Record'):
            for key in keys:
                value = station.find(key).text
                data[key] = value
    except Exception as e:
        print(e)
        # return none and 500 if any errors happen
        return make_response({'Error':'Could not fetch data'}, 400)
    # return json results and send 200
    return make_response(data, 200)
