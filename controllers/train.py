from bson.json_util import dumps
from flask import Blueprint, make_response, request
import requests
import json
from cerberus import Validator
# create the blueprint (controller) for the routes
trains = Blueprint('trains', __name__)


def schema_validator(token=None, route=None):
    schema = {'token':{'type':'string', 'maxlength':36}, 'route':{'type':'string','maxlength':10}}
    v = Validator(schema)
    input_info = {}
    for info in [('token', token), ('route', route)]:
        info_key, info_value = info
        if info_value:
            input_info[info_key] = info_value
    return v.validate(input_info)


# create GET endpoint to return all routes
@trains.route('/trains/find', methods=['GET'])
def find_train():
    try:
        arrival = request.args.get('arrival')
        departure = request.args.get('departure')
        departure_date = request.args.get('departure date')
    except:
        return make_reponse({'Error':'Missing or invalid input'}, 400)

    try:
        result = requests.get(f'https://luxapi.verbinteractive.com/api/TrainStatus?arrival={arrival}&departure={departure}&departureDate={departure_date}')
        result_text = result.text
        result_dump = json.dumps(result_text)
        data = json.loads(result_dump)
    except:
        return make_response({'Error':'Could not fetch data'}, 500)

    return make_response(data, 200)

