from bson.json_util import dumps
from flask import Blueprint, make_response, request
import requests
import json
import datetime
from cerberus import Validator

# create the blueprint (controller) for the routes
trains = Blueprint('trains', __name__)


def schema_validator(arrival=None, departure=None, departure_date=None):
    schema = {'arrival':{'type':'string', 'maxlength':3}, 'departure':{'type':'string','maxlength':3}, 'departure_date':{'type':'string', 'maxlength':10}}
    v = Validator(schema)
    input_info = {}
    all_vali = [('arrival', arrival), ('departure', departure), ('departure_date', departure_date)]
    for info in all_vali:
        info_key, info_value = info
        if info_value:
            input_info[info_key] = info_value
    return v.validate(input_info)

def trip_info(trip):
    try:
        trip_data = {}
        train_keys = ['origin','destination','train','consistNumber','estimatedDeparture',
               'scheduledDeparture','actualDeparture','scheduledArrival','estimatedArrival',
               'actualArrival','actualArrivalPlatform','actualDeparturePlatform',
               'arrivalPlatform','arrivalStatus','departurePlatform','legs']
        leg_keys = ['actualArrival','actualDeparture','estimatedArrival','estimatedDeparture',
                'arrivalStatus','consistNumber','isCancelled','actualArrivalPlatform',
                'actualDeparturePlatform','arrivalPlatform','departurePlatform','legStatus',
                'origin','scheduledArrival','scheduledArrivalPlatform','scheduledDeparture',
                'scheduledDeparturePlatform','train']
        for key in train_keys:
            trip_value = trip[key]
            if key == 'legs':
                leg_data = []
                for leg in trip_value:
                    leg_info = {}
                    for leg_key in leg_keys:
                        leg_info[leg_key] = leg[leg_key]
                    leg_data.append(leg_info)
                trip_data[key] = leg_data
                continue
            trip_data[key] = trip_value
        return trip_data
    except:
        return False

# create GET endpoint to return all routes
@trains.route('/trains/find', methods=['GET'])
def find_train():
    try:
        arrival = request.args.get('arrival')
        departure = request.args.get('departure')
        departure_date = request.args.get('departure date')
        datetime.datetime.strptime(departure_date, '%Y-%M-%d')
        assert(schema_validator(arrival, departure, departure_date))
    except:
        return make_response({'Error':'Missing or invalid input'}, 400)

    try:
        result = requests.get(f'https://luxapi.verbinteractive.com/api/TrainStatus?arrival={arrival}&departure={departure}&departureDate={departure_date}')
        result_text = result.text
        result_dump = json.dumps(result_text)
        data = json.loads(result_dump)
        data_json = result.json()
        train_data = list(map(trip_info, data_json))
        assert(train_data)

    except:
        return make_response({'Error':'Could not fetch data'}, 500)
    if not data:
        return make_response({'Error':'No data'}, 404)
    return make_response(json.dumps(train_data), 200)

