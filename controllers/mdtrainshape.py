from bson.json_util import dumps
from flask import Blueprint, make_response, request
import xml.etree.ElementTree as ET
from cerberus import Validator
import requests
import json
# create the blueprint (controller) for the routes
mdtrainshape = Blueprint('mdtrainshape', __name__)

def schema_validator(line_id):
    schema = {'line':{'type':'string','maxlength':3}}
    v = Validator(schema)
    input_info = {'line': line_id}
    return v.validate(input_info)

@mdtrainshape.route('/mdtrainshape/find', methods=['GET'])
def find_mdtrainshape():
    # parse id param from call
    try:
        line_id = request.args.get('line_id')
        assert(schema_validator(line_id))
    except Exception as e:
        print(e)
        # return error message and 400 if it throws an exeption
        return make_response({'Error': 'Missing or invalid input'}, 400)
    try:
        result = requests.get(f'http://www.miamidade.gov/transit/WebServices/TrainMapShape/?LineID={line_id}', verify=False)
        # turn result into xml and access root
        root = ET.fromstring(result.text)
        data = []
        # iterate over all records in root
        for station in root.findall('Record'):
            info = {}
            for tag in station:
                value = tag.text
                info[tag.tag] = value
            data.append(info)
    except Exception as e:
        print(e)
        # return none and 500 if any errors happen
        return make_response({'Error':'Could not fetch data'}, 400)
    # return json results and send 200
    return make_response(json.dumps(data), 200)
