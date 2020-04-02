from bson.json_util import dumps
from flask import Blueprint, make_response, request
import requests
import json
import datetime
from cerberus import Validator

# create the blueprint (controller) for the trains
trains = Blueprint('trains', __name__)

# schema validator
def schema_validator(arrival=None, departure=None, departure_date=None):
    schema = {'arrival':{'type':'string', 'maxlength':3}, 'departure':{'type':'string','maxlength':3}, 'departure_date':{'type':'string', 'maxlength':10}}
    v = Validator(schema)
    input_info = {}
    # the proper string pair with its variable
    all_vali = [('arrival', arrival), ('departure', departure), ('departure_date', departure_date)]
    # iterate over all passed variable
    for info in all_vali:
        # unpack tuple
        info_key, info_value = info
        # if the variable is not 'None' pass it through schema validator
        if info_value:
            input_info[info_key] = info_value
    return v.validate(input_info)

# getting trip info from each train
def trip_info(trip):
    # variable to store the info we actually want
    trip_data = {}
    # array with the keys we want
    train_keys = ['origin','destination','train','consistNumber','estimatedDeparture',
               'scheduledDeparture','actualDeparture','scheduledArrival','estimatedArrival',
               'actualArrival','actualArrivalPlatform','actualDeparturePlatform',
               'arrivalPlatform','arrivalStatus','departurePlatform','legs']
    # array with the keys we want from 'leg'
    leg_keys = ['actualArrival','actualDeparture','estimatedArrival','estimatedDeparture',
                'arrivalStatus','consistNumber','isCancelled','actualArrivalPlatform',
                'actualDeparturePlatform','arrivalPlatform','departurePlatform','legStatus',
                'origin','scheduledArrival','scheduledArrivalPlatform','scheduledDeparture',
                'scheduledDeparturePlatform','train']
    for key in train_keys:
        # check if key is missing
        try:
            # get value of the current key
            trip_value = trip[key]
            if key == 'legs':
                # array to hold all 'leg' dictionaries with keys we want
                leg_data = []
                for leg in trip_value:
                    # variable to store the info we want from 'leg'
                    leg_info = {}
                    for leg_key in leg_keys:
                        leg_info[leg_key] = leg[leg_key]
                    leg_data.append(leg_info)
                trip_data[key] = leg_data
                continue
            trip_data[key] = trip_value
        # if key missing assign empty string
        except:
            trip_data[key] = ''
    return trip_data

# create GET endpoint to return all routes
@trains.route('/trains/find', methods=['GET'])
def find_train():
    try:
        arrival = request.args.get('arrival')
        departure = request.args.get('departure')
        departure_date = request.args.get('departure date')
        # check if departure date is in proper format
        datetime.datetime.strptime(departure_date, '%Y-%M-%d')
        # validate arguments
        assert(schema_validator(arrival, departure, departure_date))
    except:
        return make_response({'Error':'Missing or invalid input'}, 400)

    try:
        # main api call, returns array
        result = requests.get(f'https://luxapi.verbinteractive.com/api/TrainStatus?arrival={arrival}&departure={departure}&departureDate={departure_date}')
        # turn request object into text
        result_text = result.text
        # dump text as string
        result_dump = json.dumps(result_text)
        # load string
        data = json.loads(result_dump)
        # jsonify result
        data_json = result.json()
        # pass each array element to method
        train_data = list(map(trip_info, data_json))

    except:
        return make_response({'Error':'Could not fetch data'}, 500)
    # since data is array dump it as string
    return make_response(json.dumps(train_data), 200)

