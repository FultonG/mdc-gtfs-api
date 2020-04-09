from bson.json_util import dumps
from flask import Blueprint, make_response, request
import xml.etree.ElementTree as ET
from cerberus import Validator
import requests
import json
# create the blueprint (controller) for the routes
mdshape = Blueprint('shape', __name__)

def schema_validator(shape_id):
    schema = {'shape':{'type':'string','maxlength':6}}
    v = Validator(schema)
    input_info = {'shape': shape_id}
    return v.validate(input_info)

@mdshape.route('/mdshape/find', methods=['GET'])
def find_mdshape():
    # parse id param from call
    try:
        shape_id = request.args.get('shape_id')
        assert(schema_validator(shape_id))
    except Exception as e:
        print(e)
        # return error message and 400 if it throws an exeption
        return make_response({'Error': 'Missing or invalid input'}, 400)
    try:
        result = requests.get(f'http://www.miamidade.gov/transit/WebServices/BusRouteShape/?ShapeID={shape_id}', verify=False)
        # turn result into xml and access root
        root = ET.fromstring(result.text)
        data = []
        # iterate over all records in root
        for shape in root.findall('Record'):
            lat = shape.find('Latitude').text
            lon = shape.find('Longitude').text
            data.append([lat, lon])
    except Exception as e:
        print(e)
        # return none and 500 if any errors happen
        return make_response({'Error':'Could not fetch data'}, 400)
    # return json results and send 200
    return make_response(json.dumps(data), 200)
