from bson.json_util import dumps
from flask import Blueprint, make_response, request
import xml.etree.ElementTree as ET
from cerberus import Validator
import requests
import json
# create the blueprint (controller) for the routes
mdshapeid = Blueprint('mdshapeid', __name__)

def schema_validator(trip_id):
    schema = {'trip':{'type':'string','maxlength':7}}
    v = Validator(schema)
    input_info = {'trip': trip_id}
    return v.validate(input_info)

@mdshapeid.route('/mdshapeid/find', methods=['GET'])
def find_mdshapeid():
    # parse id param from call
    try:
        trip_id = request.args.get('trip')
        assert(schema_validator(trip_id))
    except Exception as e:
        print(e)
        # return error message and 400 if it throws an exeption
        return make_response({'Error': 'Missing or invalid input'}, 400)
    try:
        result = requests.get(f'http://www.miamidade.gov/transit/WebServices/BusRouteShapesByTrip/?TripID={trip_id}', verify=False)
        # turnr result into XML and access root
        root = ET.fromstring(result.text)
        # only one record is returned so access that record
        # with the first [0] and since that record only holds
        # on tag, ShapeID, access it with the other [0]
        shape_id = root[0][0].text
        data = {'shapeID':shape_id}
    except Exception as e:
        print(e)
        # return none and 500 if any errors happen
        return make_response({'Error':'Could not fetch data'}, 400)
    # return json results and send 200
    return make_response(data, 200)
